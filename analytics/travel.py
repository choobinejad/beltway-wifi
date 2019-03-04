from datetime import datetime, timedelta
from collections import Counter
from hashlib import sha256
from utilities import common


def _generate_companion_query(start, end, geohash, radius):
    companion = \
        {
            "query": {
                "bool": {
                    "must": [
                        {"range": {
                            "event_time": {
                                "gte": start,
                                "lte": end,
                            }
                        }}
                    ],
                    "filter": {
                        "geo_distance": {
                            "distance": radius,
                            "location": geohash
                        }
                    }
                }
            },
            "size": 0,
            "aggs": {
                "companions": {
                    "terms": {
                        "field": "source",
                        "size": 100
                    }
                }
            }
        }
    return companion


def find_companions(es, source, index=True):
    print('\n')
    start = datetime.now()
    query = \
        {
            "query": {
                "bool": {
                    "must": [
                        {"term": {
                            "source": {
                                "value": source
                            }
                        }},
                        {"range": {
                            "event_time": {
                                "gte": "now-2h"
                            }
                        }}
                    ]
                }
            },
            "size": 0,
            "aggs": {
                "date_histogram": {
                    "date_histogram": {
                        "field": "event_time",
                        "interval": "5m"
                    },
                    "aggs": {
                        "location": {
                            "geohash_grid": {
                                "field": "location",
                                "precision": 8
                            }
                        }
                    }
                }
            }
        }
    r = es.search('network_events', '_doc', body=query)['aggregations']['date_histogram']['buckets']
    r = {b['key']: [bb['key'] for bb in b['location']['buckets']] for b in r}
    r = {k: v for k, v in r.items() if len(v) > 1}
    unique_companions = set()
    results = []
    counter = Counter()
    query_count = 0
    parent_count = 0
    for timestamp, geohashes in r.items():
        for geohash in geohashes:
            query_count += 1
            companions = es.search('network_events', '_doc', body=_generate_companion_query(
                timestamp,
                (datetime.fromtimestamp(timestamp/1000) + timedelta(minutes=5)).timestamp()*1000,
                geohash,
                '100m'
            ))['aggregations']['companions']['buckets']
            companions = [c['key'] for c in companions if c['key'] != source]
            counter.update(companions)
            if len(companions) > 0:
                results.append((timestamp, geohash, companions))
            unique_companions.update(companions)
        parent_count += 1
        common.progress(parent_count, len(r))

    end = datetime.now()
    print("\n{} queries | {} seconds | {} seconds per query".format(
        query_count, (end-start).seconds, (end-start).seconds/(query_count + 1))
    )

    case_id = sha256(source.encode()).hexdigest()
    es.index(
        'cases',
        '_doc',
        body=dict(
            case_id=case_id,
            updated=datetime.utcnow().isoformat(),
            subject='John Q. Private',
            subject_mac=source,
            unique_companions=list(unique_companions),
            counted_incidents=[{'companion': k, 'count': v} for k, v in counter.items()],
            incident_detail=[
                dict(
                    companions=row[2],
                    location=row[1],
                    time_range=dict(
                        gte=datetime.fromtimestamp(row[0]/1000.0).isoformat(),
                        lte=(datetime.fromtimestamp(row[0]/1000.0) + timedelta(seconds=300)).isoformat()
                    )
                ) for row in results
            ]
        ),
        id=case_id
    )

    return counter, results[:10], unique_companions

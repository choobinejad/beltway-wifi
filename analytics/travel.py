import sys
from datetime import datetime, timedelta
from collections import Counter


def _progress(count, total, status=''):
    bar_len = 100
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[{}] {}{} ...{}\r'.format(bar, percents, '%', status))
    sys.stdout.flush()


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


def find_companions(source, es):
    print('\n' * 2)
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
        _progress(parent_count, len(r))

    end = datetime.now()
    print("\n{} queries | {} seconds | {} seconds per query".format(
        query_count, (end-start).seconds, (end-start).seconds/(query_count + 1))
    )
    return counter, results[:10], unique_companions

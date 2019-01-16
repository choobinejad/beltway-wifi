import time
import random
from datetime import datetime, timedelta
from elasticsearch.helpers import bulk


def create_es_query(minutes, size, override_range=None, density_agg=False):
    query = dict(
        query=dict(
            bool=dict(
                must=[
                    {"range": {"heartbeat": {"lte": "now-{}m".format(str(minutes))}}}
                ],
                must_not=[
                    {"geo_polygon": {
                        "location": {
                            "points": [
                                [-77.045190, 39.004399], [-77.034190, 39.005399], [-77.003890, 39.000199],
                                [-77.018490, 38.983399], [-77.047990, 38.986099], [-77.045190, 39.004399]
                            ]
                        }
                    }},
                    {"term": {
                        "gateway": "ab:ab:ab:11:11:11"
                    }}
                ]
            )
        ),
        sort=[{"heartbeat": {"order": "asc"}}],
        size=size,
        _source=["heartbeat"]
    )
    if override_range:
        query['query']['bool']['must'][0]['range']['heartbeat'] = override_range
    if density_agg:
        query['aggs'] = {
            "a": {"date_histogram": {"field": "heartbeat", "interval": "10s"}},
            "b": {"max_bucket": {"buckets_path": "a._count"}}
        }
    return query


def _generate_heartbeats(es):
    docs = es.search('towers,waps', '_doc', body=create_es_query(31, 299))
    if docs['hits']['total'] == 0:
        time.sleep(5)
    docs = docs['hits']['hits']
    densest_bucket_start = es.search(
        'towers,waps', '_doc', body=create_es_query(2, 0, density_agg=True)
    )['aggregations']['b']['keys'][0][:-5]
    densest_bucket_end = (
            datetime.strptime(densest_bucket_start, '%Y-%m-%dT%H:%M:%S') + timedelta(seconds=10)
    ).isoformat()
    docs += es.search(
        'towers,waps',
        '_doc',
        body=create_es_query(
            2,
            random.randint(50, 200),
            override_range=dict(gte=densest_bucket_start, lte=densest_bucket_end)
        )
    )['hits']['hits']

    for doc in docs:
        yield dict(
            _op_type='update',
            _index=doc['_index'],
            _type='_doc',
            _id=doc['_id'],
            doc=dict(heartbeat=datetime.utcnow().isoformat())
        )


def update_oldest_heartbeats(es):
    while True:
        result = bulk(es, _generate_heartbeats(es))
        if len(result[1]) > 0:
            print('Problem updating infra heartbeats...', result)
        else:
            print('Indexed Infra Heartbeats ({})'.format(result[0]))
        time.sleep(random.randint(1, 5))

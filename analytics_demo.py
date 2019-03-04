from datetime import datetime
import random
import fire
from prettytable import PrettyTable
from utilities.elastic import get_elastic_client
from analytics.travel import find_companions


def companions(es_host, user, password, mac):
    es = get_elastic_client(es_host, user, password)
    if mac == 'recommend':
        mac = suggest(es_host, user, password).replace('\n', '')
        print('\nSkeiNet recommends analyzing this valued customer: {}'.format(mac))
    counter, result, unique_companions = find_companions(es, mac)

    # Print out the companions list
    print('\nThe `companions` algorithm identified {} unique companions for {}. They are:'.format(
        len(unique_companions), mac
    ))
    print(', '.join(list(unique_companions)[:10]) + ', ...')

    # Print out the raw result records, bucketed by time and space dimensions
    raw = PrettyTable()
    raw.field_names = ['Timestamp', 'Geohash', 'Companions']
    for r in result:
        truncated = '...' if len(r[2]) > 3 else ''
        raw.add_row([datetime.fromtimestamp(r[0]/1000.0).isoformat(), r[1], ', '.join(r[2][:3]) + truncated])
    raw.add_row(['...', '...', '...'])
    print('\nHere is a sample of the raw results:')
    print(raw)

    # Print out the inverted summary of closest companions
    indexed = PrettyTable()
    indexed.field_names = ['Companion', 'Occurrences']
    for k, v in counter.most_common(10):
        indexed.add_row([k, str(v)])
    indexed.add_row(['...', '...'])
    print('\nThe most significantly correlated companions for {} are:'.format(mac))
    print(indexed)


def suggest(es_host, user, password):
    es = get_elastic_client(es_host, user, password)
    seed = es.search(
        'network_events',
        '_doc',
        body= \
        {
            "query": {"match_all": {}},
            "size": 0,
            "aggs": {
                "top_term": {
                    "terms": {
                        "field": "source",
                        "size": random.randint(1, 10)
                    }
                }
            }
        }
    )['aggregations']['top_term']['buckets'][-1]['key']
    return '\n{}\n'.format(seed)


if __name__ == '__main__':
    fire.Fire()

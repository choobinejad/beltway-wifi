import random
from random import shuffle
import time
from datetime import datetime
from elasticsearch.helpers import bulk
from utilities.identifiers import generate_words
from utilities.geo import random_bad_gateway_point, random_dc_point


def _retrieve_bad_gateways(es):
    bad_gateway_waps = [b['key'] for b in es.search(
        'waps', '_doc', body=\
        {
          "query": {
            "bool": {
              "must": [
                {"geo_polygon": {"location": {"points": [
                    [-77.045190, 39.004399], [-77.034190, 39.005399], [-77.003890, 39.000199],
                    [-77.018490, 38.983399], [-77.047990, 38.986099], [-77.045190, 39.004399]
                ]}}}
              ]
            }
          },
          "size": 0,
          "aggs": {
            "waps": {
              "terms": {
                "field": "ssid.keyword",
                "size": 100
              }
            }
          }
        }
    )['aggregations']['waps']['buckets']]
    return bad_gateway_waps


def _get_angry_customers(es):
    query = \
        {
          "query": {
            "bool": {
              "must": [
                {"geo_polygon": {"location": {"points": [
                    [-77.045190, 39.004399], [-77.034190, 39.005399], [-77.003890, 39.000199],
                    [-77.018490, 38.983399], [-77.047990, 38.986099], [-77.045190, 39.004399]
                ]}}}
              ]
            }
          },
          "size": 0,
          "aggs": {
            "macs": {
              "terms": {
                "field": "source",
                "size": random.randint(10, 20)
              }
            }
          }
        }
    angry_customers = [
        b['key'] for b in es.search('network_events', '_doc', body=query)['aggregations']['macs']['buckets']
    ][:-1]
    shuffle(angry_customers)
    return angry_customers


def _generate_angry_customer_docs(es, min_cx=1, max_cx=3):
    bad_gateway_waps = _retrieve_bad_gateways(es)
    colocation = random_dc_point()
    for mac in _get_angry_customers(es):
        # This doc places the `mac` in the bad service zone.
        record = dict(
            _op_type='index',
            _index='network_events',
            _type='_doc',
            event_time=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(5, 10)).isoformat(),
            source=mac,
            source_class='MAC Address',
            action='probe request',
            destination=[random.choice(bad_gateway_waps) for i in range(random.randint(min_cx, max_cx))],
            destination_class='SSID',
            location=random_bad_gateway_point(),
            premium=True
        )
        yield record
        # This doc places the `mac` at some other random point in the area where it will be colocated with
        # all the macs in this batch.
        record = dict(
            _op_type='index',
            _index='network_events',
            _type='_doc',
            event_time=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(5, 10)).isoformat(),
            source=mac,
            source_class='MAC Address',
            action='probe request',
            destination=[generate_words() for j in range(random.randint(1, 3))],
            destination_class='SSID',
            location=colocation,
            admin_cheat_note='colocation: {}'.format(colocation),
            premium=True
        )
        yield record
        # Create another colocation event, a bit further in the past, to support dwell/spans.
        record = dict(
            _op_type='index',
            _index='network_events',
            _type='_doc',
            event_time=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(20, 40)).isoformat(),
            source=mac,
            source_class='MAC Address',
            action='probe request',
            destination=[generate_words() for j in range(random.randint(1, 3))],
            destination_class='SSID',
            location=colocation,
            admin_note='colocation: {}'.format(colocation),
            premium=True
        )
        yield record


def generate_angry_customer_probes(es):
    while True:
        result = bulk(es, _generate_angry_customer_docs(es))
        if len(result[1]) > 0:
            print('Problem indexing angry customer probe activity...', result)
        else:
            print('Indexed Angry Customer Probes ({})'.format(result[0]))
        time.sleep(random.randint(10, 30))

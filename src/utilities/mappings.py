import json
import time


def _put_towers_mapping(es):
    if not es.indices.exists('towers'):
        with open('./utilities/config/cell_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.create('towers', body=mapping)
        print('Configured "towers" mapping')
    else:
        print('"towers" mapping already configured')


def _put_waps_mapping(es):
    if not es.indices.exists('waps'):
        with open('./utilities/config/waps_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.create('waps', body=mapping)
        print('Configured "waps" mapping')
    else:
        print('"waps" mapping already configured')


def _put_network_activity_mapping(es):
    if not es.indices.exists_template('network_events'):
        with open('./utilities/config/network_events_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.put_template('network_events', body=mapping)
        print('Configured "network_events" template')
    else:
        print('"network_events" template already configured')


def put_all_mappings(es):
    _put_towers_mapping(es)
    _put_waps_mapping(es)
    _put_network_activity_mapping(es)
    time.sleep(1)

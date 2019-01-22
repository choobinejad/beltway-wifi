import json
import time


def _put_towers_mapping(es):
    if not es.indices.exists('towers'):
        with open('./utilities/cell_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.create('towers', body=mapping)
        print('Configured "towers" mapping')
    else:
        print('"towers" mapping already configured')


def _put_waps_mapping(es):
    if not es.indices.exists('waps'):
        es.indices.create('waps', body={
            "mappings": {
                "_doc": {
                    "properties": {
                        "location": {"type": "geo_point"},
                        "wap_point": {"type": "alias", "path": "location"},
                        "mac": {"type": "keyword"},
                        "gateway": {"type": "keyword"}
                    }
                }
            },
            "settings": {"number_of_shards": 1, "number_of_replicas": 1}
        })
        print('Configured "waps" mapping')
    else:
        print('"waps" mapping already configured')


def _put_network_activity_mapping(es):
    if not es.indices.exists('network_events'):
        es.indices.create('network_events', body={
            "mappings": {
                "_doc": {
                    "properties": {
                        "location": {"type": "geo_point"},
                        "user_point": {"type": "alias", "path": "location"},
                    },
                    "dynamic_templates": [
                        {
                            "strings_as_keywords": {
                                "match_mapping_type": "string",
                                "mapping": {
                                    "type": "keyword"
                                }
                            }
                        }
                    ]
                }
            },
            "settings": {"number_of_shards": 1, "number_of_replicas": 1}
        })
        print('Configured "network_events" mapping')
    else:
        print('"network_events" mapping already configured')


def _put_cases_mapping(es):
    if not es.indices.exists('cases'):
        with open('./utilities/cases_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.create('cases', body=mapping)
        print('Configured "cases" mapping')
    else:
        print('"cases" mapping already configured')


def put_all_mappings(es):
    _put_towers_mapping(es)
    _put_waps_mapping(es)
    _put_network_activity_mapping(es)
    _put_cases_mapping(es)
    time.sleep(1)

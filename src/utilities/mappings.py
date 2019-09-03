import json
import time
from datetime import datetime
import requests  # TODO use only until python lib supports ILM
from requests.auth import HTTPBasicAuth  # TODO use only until python lib supports ILM


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


def _put_network_activity_mapping(es, temp_es_host, temp_es_user, temp_es_password):

    # Configure ILM
    # TODO remove requests call when Python lib supports ILM
    try:
        r = requests.get(temp_es_host, auth=HTTPBasicAuth(temp_es_user, temp_es_password)).json()['network_events']
    except KeyError:
        with open('./utilities/config/network_events_ilm_policy.json', 'r') as f:
            ilm_policy = json.load(f)
        r = requests.put(temp_es_host, auth=HTTPBasicAuth(temp_es_user, temp_es_password), json=ilm_policy)
        assert r.status_code == 200

    # Configure Index Template
    if not es.indices.exists_template('network_events'):
        with open('./utilities/config/network_events_mapping.json', 'r') as f:
            mapping = json.load(f)
        es.indices.put_template('network_events', body=mapping)
        print('Configured "network_events" template')
    else:
        print('"network_events" template already configured')

    # Bootstrap the first index for ILM rollover purposes if the alias does not exist
    if not es.indices.exists_alias('network_events'):
        with open('./utilities/config/network_events_alias.json', 'r') as f:
            alias = json.load(f)
        es.indices.put_alias(
            index='network_events_{}-000001'.format(datetime.strftime(datetime.utcnow(), '%Y.%m.%d')),
            name='network_events',
            body=alias
        )


def put_all_mappings(es):
    _put_towers_mapping(es)
    _put_waps_mapping(es)
    _put_network_activity_mapping(es)
    time.sleep(1)

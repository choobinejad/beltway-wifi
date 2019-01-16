import json
import requests
from requests.auth import HTTPBasicAuth


pattern_ids = ['towers,waps', 'waps', 'towers', 'network_events', 'towers,waps*', 'waps*', 'towers*', 'network_events*']
visualizations = [
    'Healthy WAPs', 'Stale WAPs',
    'Healthy Towers', 'Stale Towers',
    'Beltway WiFi WAPs (Reporting: DOWN)',
    'Beltway WiFi WAPs (Reporting: UP)',
    'Partner Cell Towers (Reporting: DOWN)',
    'Partner Cell Towers (Reporting: UP)',
    'Infrastructure Checkin Health',
    'Busiest SSIDs',
    'User Activity',
    'Active Users -- Most Probes',
    'Gateways w/ DOWN WAPs (Significant Terms)',
    'Gateways w/ DOWN WAPs (Terms)'
]
dashboards = ['Infrastructure', 'Users Overview', 'Infrastructure (WAPs Only)']


def get_index_patterns(kibana_base, user, password):
    storage_format = []
    for pattern_id in pattern_ids:
        pattern = requests.get(
            '{}/api/saved_objects/index-pattern/{}'.format(kibana_base, pattern_id),
            auth=HTTPBasicAuth(user, password)
        ).json()
        print(pattern)
        del pattern['id']
        del pattern['type']
        del pattern['updated_at']
        del pattern['version']
        storage_format.append(pattern)
    with open('./utilities/index_patterns.kibana', 'w') as f:
        json.dump(storage_format, f, indent=2)


def post_index_patterns(kibana_base, user, password):
    with open('./utilities/index_patterns.kibana', 'r') as f:
        index_patterns = json.load(f)

    for pattern in index_patterns:
        r = requests.post(
            url='{}/api/saved_objects/index-pattern/{}'.format(kibana_base, pattern['attributes']['title']),
            json=pattern,
            headers={'kbn-xsrf': 'it-is-an-app '},
            auth=HTTPBasicAuth(user, password)
        )
        if r.status_code not in [200, 409]:
            print(r.json())
        print('Configured index pattern: {}'.format(pattern['attributes']['title']))


def get_viz(kibana_base, user, password):
    storage_format = []
    for viz in visualizations:
        viz = requests.get(
            '{}/api/saved_objects/visualization/{}'.format(kibana_base, viz),
            auth=HTTPBasicAuth(user, password)
        ).json()
        del viz['id']
        del viz['type']
        del viz['version']
        del viz['updated_at']
        storage_format.append(viz)
    with open('./utilities/visualizations.kibana', 'w') as f:
        json.dump(storage_format, f, indent=2)


def post_viz(kibana_base, user, password):
    with open('./utilities/visualizations.kibana', 'r') as f:
        vizs = json.load(f)

    for viz in vizs:
        r = requests.post(
            url='{}/api/saved_objects/visualization/{}'.format(kibana_base, viz['attributes']['title']),
            json=viz,
            headers={'kbn-xsrf': 'it-is-an-app '},
            auth=HTTPBasicAuth(user, password)
        )
        if r.status_code not in [200, 409]:
            print(r.json())
        print('Configured Kibana visualization: {}'.format(viz['attributes']['title']))


def get_dashboards(kibana_base, user, password):
    storage_format = []
    for dashboard in dashboards:
        dashboard = requests.get(
            '{}/api/saved_objects/dashboard/{}'.format(kibana_base, dashboard),
            auth=HTTPBasicAuth(user, password)
        ).json()
        del dashboard['id']
        del dashboard['type']
        del dashboard['version']
        del dashboard['updated_at']
        storage_format.append(dashboard)
    with open('./utilities/dashboards.kibana', 'w') as f:
        json.dump(storage_format, f, indent=2)


def post_dashboards(kibana_base, user, password):
    with open('./utilities/dashboards.kibana', 'r') as f:
        dbs = json.load(f)

    for db in dbs:
        r = requests.post(
            url='{}/api/saved_objects/dashboard/{}'.format(kibana_base, db['attributes']['title']),
            json=db,
            headers={'kbn-xsrf': 'it-is-an-app '},
            auth=HTTPBasicAuth(user, password)
        )
        if r.status_code not in [200, 409]:
            print(r.json())
    print('Configured Kibana dashboard: {}'.format(db['attributes']['title']))

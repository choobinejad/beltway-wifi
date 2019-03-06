import json
import requests
from requests.auth import HTTPBasicAuth


def create_es_roles(es):
    existing_roles = es.xpack.security.get_role().keys()
    with open('./utilities/config/roles.elasticsearch', 'r') as f:
        roles = json.load(f)
    for role, body in roles.items():
        if role in existing_roles:
            print('Role "{}" already exists.'.format(role))
            continue
        es.xpack.security.put_role(role, body=body)
        print('Created security role: "{}"'.format(role))


def create_users(es, account_password):
    existing_users = es.xpack.security.get_user().keys()
    with open('./utilities/config/users.elasticsearch', 'r') as f:
        users = json.load(f)
    for user, roles in users.items():
        if user in existing_users:
            print('User "{}" already exists.'.format(user))
            continue
        body = dict(
            email='{}@nope.com'.format(user),
            full_name='{} Q. User'.format(user.capitalize()),
            password=account_password,
            roles=roles
        )
        es.xpack.security.put_user(user, body=body)
        print('Created user account: "{}" with password "{}"'.format(user, account_password))


def provision_spaces_access(kibana_base, user, password):
    with open('./utilities/config/spaces_privs.kibana', 'r') as f:
        privs = json.load(f)
    for role, config in privs.items():
        r = requests.put(
            '{}/api/security/role/{}'.format(kibana_base, role),
            headers={'kbn-xsrf': 'it-is-an-app '},
            json=config,
            auth=HTTPBasicAuth(user, password)
        )
        print('Configured the "{}" role with access to the "{}" space'.format(role, list(config['kibana']['space'].keys())))

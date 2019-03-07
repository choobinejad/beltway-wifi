import json
import random
from datetime import datetime
from hashlib import md5

from elasticsearch.helpers import parallel_bulk

from src.utilities.identifiers import generate_mac_address, generate_words


def frange(start, stop, step, precision=5):
    while start < stop:
        yield int(start * 10**precision) / 10**precision
        start += step


def generate_wap_points():
    n = 1
    latitudes = list(frange(38.7, 39.1, .003))
    longitudes = list(frange(-77.3, -76.8, .003))
    for lat in latitudes:
        for long in longitudes:
            yield n, [long, lat]
            n += 1


def generate_wap_docs():
    with open('./emitters/bad_gateway_waps.json', 'r') as f:
        # TODO this is method 1 of 3 for detecting ssid-gateway relationships
        bad_gateway_waps = json.load(f)
    for ordinal, position in generate_wap_points():
        doc = dict(
            _op_type='index',
            _index='waps',
            _type='_doc',
            _id=md5(str(position).encode()).hexdigest(),
            location=position,
            mac=generate_mac_address(oui='ab:12:c3', ordinal=ordinal),
            ssid=generate_words(),
            heartbeat=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(1, 3600)).isoformat(),
            gateway=generate_mac_address(oui='ab:ab:ab'),
        )
        if doc['_id'] in bad_gateway_waps:
            # Plant a bad gateway for some specific WAPS.
            doc['gateway'] = 'ab:ab:ab:11:11:11'
        yield doc


def index_company_wap_locations(es):
    if es.count('waps')['count'] == 22378:
        print('Skipping WAPs -- already indexed.')
        return
    for success, info in parallel_bulk(es, generate_wap_docs(), chunk_size=5000):
        if not success:
            print(success, info)

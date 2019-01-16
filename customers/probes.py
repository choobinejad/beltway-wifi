from datetime import datetime
import random
import time
from elasticsearch.helpers import bulk
from utilities.identifiers import generate_mac_address, generate_words
from utilities.geo import random_dc_point


def _generate_probe_docs(min_n=50, max_n=200, min_cx=3, max_cx=9):
    for i in range(random.randint(min_n, max_n)):
        record = dict(
            _op_type='index',
            _index='network_events',
            _type='_doc',
            event_time=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(5, 10)).isoformat(),
            source=generate_mac_address(),
            source_class='MAC Address',
            action='probe request',
            destination=[generate_words() for j in range(random.randint(min_cx, max_cx))],
            destination_class='SSID',
            location=random_dc_point()
        )
        yield record


def generate_probes(es):
    while True:
        result = bulk(es, _generate_probe_docs())
        if len(result[1]) > 0:
            print('Problem indexing probe activity...', result)
        else:
            print('Indexed Probes ({})'.format(result[0]))
        time.sleep(random.randint(1, 8))

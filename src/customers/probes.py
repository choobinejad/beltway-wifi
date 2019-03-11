import random
import time
from datetime import datetime

from elasticsearch.helpers import bulk
from utilities.geo import random_dc_point

from utilities.identifiers import generate_mac_address, generate_words, look_up_gateway


def _generate_probe_docs(es, min_n=50, max_n=200, min_cx=3, max_cx=9):
    for i in range(random.randint(min_n, max_n)):
        record = dict(
            _op_type='index',
            _index='network_events_{}'.format(datetime.utcnow().strftime('%Y.%m.%d')),
            _type='_doc',
            event_time=datetime.fromtimestamp(datetime.utcnow().timestamp()-random.randint(5, 10)).isoformat(),
            source=generate_mac_address(),
            source_class='MAC Address',
            action='probe request',
            destination=[generate_words() for j in range(random.randint(min_cx, max_cx))],
            destination_class='SSID',
            location=random_dc_point()
        )
        record['enrichments'] = dict(
            gateways=list({look_up_gateway(es, ssid) for ssid in record['destination']}),
            premium=True if int('0x' + record['source'].replace(':', ''), 0) % 5 == 0 else False
        )
        yield record


def generate_probes(es, speed=8):
    while True:
        result = bulk(es, _generate_probe_docs(es))
        if len(result[1]) > 0:
            print('Problem indexing probe activity...', result)
        else:
            print('Indexed Background Probes ({})'.format(result[0]))
        time.sleep(random.randint(1, int(speed)))

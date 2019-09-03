import threading
import time

import fire
from customers import bad_gateway_customer
from customers import probes
from emitters import cell_partners
from emitters import wap
from utilities import elastic
from utilities import kibana
from utilities import mappings
from utilities import security

from emitters import heartbeats


def run(es_host, kibana_host, user, password, new_users_password, speed=8, run_seconds=31e6, verify_certs=True):
    """
    Run the main demo.

    :param es_host: The Elasticsearch host:port to connect to. E.g. "https://acme.com:9200"
    :param kibana_host: The Kibana host:port to connect to. E.g. "https://acme.com:5601"
    :param user: ES/Kibana username to connect with
    :param password: ES/Kibana username to connect with
    :param new_users_password: the desired password for the new analyst/developer users, if they don't already exist
    :param speed: int, 1=fast, 8=default, 16=slow. Speed 8 creates about 1.5gb of `network_events` per day.
    :param run_seconds: How long to keep the demo streams alive.
    :param verify_certs: bool, whether the ES client should verify ES server certs
    :return: None
    """

    # First let's configure our Elasticsearch indices and Kibana settings
    es = elastic.get_elastic_client(es_host, user, password, verify_certs=verify_certs)
    mappings.put_all_mappings(es)
    kibana.post_index_patterns(kibana_host, user, password)
    kibana.post_viz(kibana_host, user, password)
    kibana.post_dashboards(kibana_host, user, password)
    kibana.create_spaces(kibana_host, user, password)
    kibana.post_canvas_workpad(kibana_host, user, password)
    security.create_es_roles(es)
    security.create_users(es, new_users_password)
    security.provision_spaces_access(kibana_host, user, password)

    # Let's get the lay of the land for our company and partner resources.
    threading.Thread(target=wap.index_company_wap_locations, args=[es], daemon=True).start()
    threading.Thread(target=cell_partners.index_partner_towers, args=[es], daemon=True).start()
    threading.Thread(target=heartbeats.update_oldest_heartbeats, args=[es], daemon=True).start()

    # Start some users probing
    threading.Thread(target=probes.generate_probes, args=[es, speed], daemon=True).start()
    threading.Thread(target=bad_gateway_customer.generate_angry_customer_probes, args=[es], daemon=True).start()

    # Keep-alive
    time.sleep(run_seconds)
    print('Timer! End of demo feeds.')


if __name__ == '__main__':
    fire.Fire()

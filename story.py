import sys
import time
import threading
import fire
from utilities.elastic import get_elastic_client
from utilities.kibana import *
from utilities.mappings import put_all_mappings
from emitters.wap import index_company_wap_locations
from emitters.cell_partners import index_partner_towers
from emitters.heartbeats import update_oldest_heartbeats
from customers.probes import generate_probes
from customers.bad_gateway_customer import generate_angry_customer_probes


def run(es_host, kibana_host, user, password, run_seconds=7200):
    """
    Run the main demo.

    :param es_host: The Elasticsearch host:port to connect to. E.g. "https://acme.com:9200"
    :param kibana_host: The Kibana host:port to connect to. E.g. "https://acme.com:5601"
    :param user: ES/Kibana username to connect with
    :param password: ES/Kibana username to connect with
    :param run_seconds: How long to keep the demo streams alive.
    :return: None
    """

    # First let's configure our Elasticsearch indices and Kibana settings
    es = get_elastic_client(es_host, user, password)
    put_all_mappings(es)
    post_index_patterns(kibana_host, user, password)
    post_viz(kibana_host, user, password)
    post_dashboards(kibana_host, user, password)

    # Let's get the lay of the land for our company and partner resources.
    threading.Thread(target=index_company_wap_locations, args=[es], daemon=True).start()
    threading.Thread(target=index_partner_towers, args=[es], daemon=True).start()
    threading.Thread(target=update_oldest_heartbeats, args=[es], daemon=True).start()

    # Start some users probing
    threading.Thread(target=generate_probes, args=[es], daemon=True).start()
    threading.Thread(target=generate_angry_customer_probes, args=[es], daemon=True).start()

    # Keep-alive
    time.sleep(run_seconds)
    print('Timer! End of demo feeds.')


if __name__ == '__main__':
    fire.Fire()

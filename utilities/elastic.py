from elasticsearch import Elasticsearch


def get_elastic_client(hosts, user, password):
    es = Elasticsearch(
        hosts=hosts,
        http_auth=(user, password),
        verify_certs=False
    )
    return es

from elasticsearch import Elasticsearch


def get_elastic_client(hosts, user, password, verify_certs=True):
    es = Elasticsearch(
        hosts=hosts,
        http_auth=(user, password),
        verify_certs=verify_certs
    )
    return es

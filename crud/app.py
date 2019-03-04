from flask import Flask, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


class Case:

    def __init__(self, case_id, subject, dossier=None):
        self.case_id = case_id
        self.subject = subject
        self.dossier = dossier

    def doc(self):
        return dict(
            case_id=self.case_id,
            subject=self.subject,
            dossier=self.dossier
        )


def get_cases(es):
    cases = es.search('cases', '_doc', size=200)['hits']['hits']
    cases = [
        Case(c['_id'], c['_source']['subject'], c['_source'].get('dossier')).doc() for c in cases
    ]
    return cases


def get_case(es, case_id):
    case = es.get('cases', '_doc', case_id)
    case = Case(
        case['_id'],
        case['_source']['subject'],
        case['_source'].get('dossier')
    ).doc()
    return case


def put_case(es, case_id, subject, dossier=None):
    es.index('cases', '_doc', body=Case(case_id, subject, dossier).doc(), id=case_id)
    return True


def delete_case(es, case_id):
    es.delete('cases', '_doc', case_id)
    return True


@app.route('/cases', methods=['GET', 'POST'])
def all_cases():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        put_case(app.config.es, post_data.get('case_id'), post_data.get('subject'), post_data.get('dossier'))
        response_object['message'] = 'Case created or overwritten.'
    else:
        response_object['cases'] = get_cases(app.config.es)
    return jsonify(response_object)


@app.route('/cases/<case_id>', methods=['GET', 'PUT', 'DELETE'])
def single_case(case_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object = get_case(case_id)
    if request.method == 'PUT':
        post_data = request.get_json()
        put_case(app.config.es, post_data.get('case_id'), post_data.get('subject'), post_data.get('dossier'))
        response_object['message'] = 'Case created or overwritten.'
    if request.method == 'DELETE':
        delete_case(case_id)
        response_object['message'] = 'Case deleted.'
    return jsonify(response_object)


def run(es: Elasticsearch):
    app.config.es = es
    print(111, es.ping())
    app.run()


if __name__ == '__main__':
    ES = Elasticsearch(hosts=['https://eeb61114b1844aa6a173700d5fe40098.us-east-1.aws.found.io:9243'],
                       http_auth=('elastic', '1MTjHACVlt7gzdtwI0uDSicC'))
    run(ES)

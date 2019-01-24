from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


def get_cases():
    return [{}]


def get_case(case_id):
    return {}


def put_case(case):
    CASES.append(case)
    return True


def delete_case(case_id):
    return True


@app.route('/cases', methods=['GET', 'POST'])
def all_cases():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        put_case(
            {
                'case_id': post_data.get('case_id'),
                'subject': post_data.get('subject'),
                'dossier': post_data.get('dossier')
            }
        )
        response_object['message'] = 'Case created.'
    else:
        response_object['cases'] = get_cases()
    return jsonify(response_object)


@app.route('/cases/<case_id>', methods=['GET', 'PUT', 'DELETE'])
def single_case(case_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object = get_case(case_id)
    if request.method == 'PUT':
        post_data = request.get_json()
        put_case(
            {
                'case_id': post_data.get('case_id'),
                'subject': post_data.get('subject'),
                'dossier': post_data.get('dossier')
            }
        )
        response_object['message'] = 'Case created or overwritten.'
    if request.method == 'DELETE':
        delete_case(case_id)
        response_object['message'] = 'Case deleted.'
    return jsonify(response_object)


def run():
    app.run()


if __name__ == '__main__':
    app.run()

### To-Do: Configure CORS to only allow specific requests. Very important!

from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

MATRIX = [
  {
    "id": uuid.uuid4().hex,
    "width": 5,
    "height": 2,
    "x": 2,
    "y": 2,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 3,
    "height": 2,
    "x": 3,
    "y": 2,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 1,
    "height": 2,
    "x": 4,
    "y": 2,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 2,
    "height": 8,
    "x": 1,
    "y": 3,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "title": "Conditional expression (MADs)",
    "width": 5,
    "height": 8,
    "x": 2,
    "y": 3,
    "isActive": True
  },
  {
    "id": uuid.uuid4().hex,
    "title": "Hfq Co-IP",
    "width": 3,
    "height": 8,
    "x": 3,
    "y": 3,
    "isActive": True
  },
  {
    "id": uuid.uuid4().hex,
    "title": "Median expression (TPM)",
    "width": 1,
    "height": 8,
    "x": 4,
    "y": 3,
    "isActive": True
  },
  {
    "id": uuid.uuid4().hex,
    "width": 2,
    "height": 8,
    "x": 5,
    "y": 3,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 5,
    "height": 2,
    "x": 2,
    "y": 4,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 3,
    "height": 2,
    "x": 3,
    "y": 4,
    "isActive": False
  },
  {
    "id": uuid.uuid4().hex,
    "width": 1,
    "height": 2,
    "x": 4,
    "y": 4,
    "isActive": False
  }
]

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('works!')

def remove_matrix(matrix_id):
    for matrix in MATRIX:
        if matrix['id'] == matrix_id:
            MATRIX.remove(matrix)
            return True
    return False

@app.route('/matrix', methods=['GET', 'POST'])
def all_matrix():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        MATRIX.append({
            'title': post_data.get('title'),
            'id': uuid.uuid4().hex,
            "width": post_data.get('width'),
            'height': post_data.get('height'),
            'x': post_data.get('x'),
            'y': post_data.get('y'),
            'isActive': post_data.get('isActive')
        })
        response_object['message'] = 'Matrix added!'
    else:
        response_object['matrix'] = MATRIX
    return jsonify(response_object)

@app.route('/matrix/<matrix_id>', methods=['PUT', 'DELETE'])
def single_matrix(matrix_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        remove_matrix(matrix_id)
        response_object['message'] = 'Matrix updated!'
    if request.method == 'DELETE':
        remove_matrix(matrix_id)
        response_object['message'] = 'Matrix removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    app.run()

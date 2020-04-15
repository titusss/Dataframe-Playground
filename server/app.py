# To-Do: Configure CORS to only allow specific requests. Very important!

import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid
import pandas as pd
import json
# from clustergrammer import Network

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

INPUT = [
    {

    }
]

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
app.secret_key = "super secret key"  # INSECURE AND FOR DEBUGGING PURPOSES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, resources={r'/*': {'origins': '*'}}) # enable CORS

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_matrix(matrix_id):
    for matrix in MATRIX:
        if matrix['id'] == matrix_id:
            MATRIX.remove(matrix)
            return True
    return False

@app.route('/matrix', methods=['GET', 'POST'])
def all_matrix():
    response_object = {'status': 'success'}
    response_object['matrix'] = MATRIX
    return jsonify(response_object)
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        dataList = json.loads(request.form['form'])
        print(dataList)
        print(type(dataList))
        print(dataList['title'])
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "success"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/matrix/<matrix_id>', methods=['PUT', 'DELETE'])
def single_matrix(matrix_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_matrix(matrix_id)
        MATRIX.append({
            'title': post_data.get('title'),
            'id': uuid.uuid4().hex,
            "width": post_data.get('width'),
            'height': post_data.get('height'),
            'x': post_data.get('x'),
            'y': post_data.get('y'),
            'isActive': post_data.get('isActive')
        })
        response_object['message'] = 'Matrix updated!'
    if request.method == 'DELETE':
        remove_matrix(matrix_id)
        response_object['message'] = 'Matrix removed!'
    return jsonify(response_object)

# Module for converting .csv to tab-seperated .txt


def export_matrix_tsv(input_file, cat_amount):
    # Import a csv and load it into pandas dataframe.
    df = pd.read_csv(input_file)
    # Append category title string before values for all cat columns.
    df[df.columns[0:cat_amount]] = df.columns[0:cat_amount] + \
        ': ' + df[df.columns[0:cat_amount]].astype(str)
    # Remove the category titles from first row.
    for i in range(cat_amount):
        df = df.rename(columns={df.columns[i]: ''})
    # Export the data frame as tab-seperated .txt.
    df.to_csv('output_matrix.txt', sep='\t', index=False)
    print('Output file has been generated and saved.')
    return df

# Module for convertig tab-seperated .txt into clustergrammer-ready json


def make_json(MatrixName):
    # This creates a network and loads it into a file.
    net = Network()
    net.load_file(MatrixName + '.txt')
    net.cluster(dist_type='cos', views=['N_row_sum', 'N_row_var'], dendro=True,
                sim_mat=True, filter_sim=0.1, calc_cat_pval=False, enrichrgram=False, run_clustering=True)
    # write jsons for front-end visualizations
    net.write_json_to_file('viz', 'json/mult_view.json', 'indent')
    net.write_json_to_file(
        'sim_row', 'json/mult_view_sim_row.json', 'no-indent')
    net.write_json_to_file(
        'sim_col', 'json/mult_view_sim_col.json', 'no-indent')


if __name__ == '__main__':
    app.run()

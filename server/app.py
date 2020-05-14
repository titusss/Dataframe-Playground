# To-Do: Configure CORS to only allow specific requests. Very important!

import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid
import pandas as pd
import json
import process_file
import upload_to_db
import visualize
from pymongo import MongoClient
from bson.json_util import loads, dumps, ObjectId

client = MongoClient()
db = client.projectname
visualizations = db.visualizations


UPLOAD_FOLDER = '/static' # Change this to /uploads in production
ALLOWED_EXTENSIONS_MATRIX = {'txt', 'xlsx', 'csv'}
ALLOWED_EXTENSIONS_ICON = {'svg', 'png', 'jpg', 'jpeg', 'gif'}
vis_plugin = "clustergrammer"
VIS_PATH = [""]
PLUGINS = [
    {
        "url": "",
        "name": "SandDance", 
        "desc": "Microsoft's 2D & 3D data exploration tool.",
        "icon": "sanddance_logo.svg"
    },
    {
        "url": "http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/", 
        "name": "Clustergrammer", 
        "desc": "Clustering Heatmap by Ma'ayan Laboratory", 
        "icon": "clustergrammer_preview.svg"
    }
]
MATRIX = [
    {
        "id": uuid.uuid4().hex,
        "width": 5,
        "height": 5,
        "x": 2,
        "y": 2,
        "isActive": False
    }
]
DB_ENTRY_MOCKUP = {
    'active_matrices': [],
    'transformed_dataframe': [],
    'dataframes': [],
    'preview_matrices': MATRIX,
    'vis_link': ''
}


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.secret_key = "super secret key"  # INSECURE AND FOR DEBUGGING PURPOSES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
# CORS(app, resources={r'/*': {'origins': '*'}}) # enable CORS

if __name__ == '__main__':
    app.run(threaded = True)

def allowed_file(filename, extension_whitelist):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extension_whitelist

def remove_matrix(matrix_id):
    for matrix in MATRIX:
        if matrix['id'] == matrix_id:
            MATRIX.remove(matrix)
            return True
    return False

@app.route('/')
def helloWorld():
    return "Hello world!"

@app.route('/plugins', methods=['GET', 'POST'])
def add_plugin():
    if request.method == 'POST':
        file, dataList, extension, filepath, filename = upload_file(request, ALLOWED_EXTENSIONS_ICON, "/Users/titusebbecke/Documents/Work/Helmholtz/2020/Experiments/2003_Hiri_VueBootstrap/hzi_vis_03/public/src/assets")
        dataList['icon'] = filename # Change this: Deliver static image from webserver not from flask
        PLUGINS.append(dataList)
        print("PLUGINS: ", PLUGINS)
        return jsonify(respond_data('plugin_list', PLUGINS))
    elif request.method == 'GET':
        print('method: GET: ', PLUGINS)
        return jsonify(respond_data('plugin_list', PLUGINS))


@app.route('/config', methods=['GET', 'POST'])
def respond_config():
    if request.form['url'] != 'undefined':
        db_entry_id = ObjectId(loads(request.form['url']))
        db_entry = db.visualizations.find_one({"_id": db_entry_id})
        db_entry['_id'] = str(db_entry['_id'])
        print(db_entry)
        textfile = open('textfile.txt', 'w')
        textfile.write(str(db_entry))
        textfile.close()
        return jsonify({'db_entry': db_entry})
    else:
        print('jjjjj')
        return dumps({'db_entry': DB_ENTRY_MOCKUP})

@app.route('/matrix', methods=['GET', 'POST'])
def all_matrix():
    return jsonify(respond_data('matrix', MATRIX))
    
@app.route('/upload', methods=['GET', 'POST'])
def add_matrix():
    if request.method == 'POST':
        file, metadata, extension = upload_file(request, ALLOWED_EXTENSIONS_MATRIX)
        db_entry_id = process_file.main(file, metadata, extension, visualizations, vis_plugin)
        # print(db.visualizations.find_one({"_id": db_entry_id}))
        return dumps({'db_entry_id': db_entry_id})
    else: 
        return "method unclear"

def respond_data(label, payload):
    response_object = {'status': 'success'}
    response_object[label] = payload
    return response_object

def upload_file(request, extension_whitelist):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    metadata = json.loads(request.form['form'])
    # If user does not select file, browser also submit an empty part without filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename, extension_whitelist):
        extension = os.path.splitext(file.filename)[1]
    return file, metadata, extension

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/matrix/<matrix_id>', methods=['PUT', 'DELETE'])
def single_matrix(matrix_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        response_object['message'] = 'Matrix updated!'
    if request.method == 'DELETE':
        make_preview(False, False, False, matrix_id)
        # remove_matrix(matrix_id)
        response_object['message'] = 'Matrix removed!'
    return jsonify(response_object)

def make_preview(input_file, extension, dataList, remove_id):
    MATRIX.clear()
    MATRICES, DATAFRAME, db_data_id = process_file.process_upload(input_file, extension.lower(), dataList, remove_id)
    for i in range(len(MATRICES)):
        MATRIX.append(MATRICES[i])
    return DATAFRAME

print('ran')
client.close()
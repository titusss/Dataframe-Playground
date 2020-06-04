# To-Do: Configure CORS to only allow specific requests. Very important!

import os
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid
import json
import process_file
import visualize
from pymongo import MongoClient
from bson.json_util import loads, dumps, ObjectId

# variables
UPLOAD_FOLDER = '/static' # NOTE: Change this to /uploads in production
ALLOWED_EXTENSIONS_MATRIX = {'txt', 'xlsx', 'csv'}
ALLOWED_EXTENSIONS_ICON = {'svg', 'png', 'jpg', 'jpeg', 'gif'}
PRE_CONFIGURED_PLUGINS = [ObjectId('5ed6374fdaf88ae74e38f105')]
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
    'preview_matrices': MATRIX,
    'vis_links': [],
    'plugins_id': PRE_CONFIGURED_PLUGINS
}
# MongoDB
client = MongoClient()
db = client.projectname
visualizations = db.visualizations
plugins = db.plugins

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
# app.secret_key = "super secret key"  # NOTE: INSECURE AND FOR DEBUGGING PURPOSES
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r'/*': {'origins': '*'}}) # enable CORS
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(threaded = True)

def allowed_file(filename, extension_whitelist):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extension_whitelist

# @app.route('/',methods = ['GET','POST'])
# def helloWorld():
#     print('hello world')
#     return "Hello world!"

@app.route('/locked', methods=['POST'])
def lock_session():
    from pymongo import MongoClient
    url = json.loads(request.form['url'])
    print('URL: ', url)
    db.visualizations.update_one({'_id': ObjectId(url)}, {'$set': {'locked': True}})
    return "success"

@app.route('/plugins', methods=['POST'])
def add_plugin():
    import pandas as pd
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    metadata = json.loads(request.form['form'])
    source, extension = upload_file(request, ALLOWED_EXTENSIONS_ICON, metadata)
    plugin_name = secure_filename(source.filename)
    source.save(os.path.join("/Users/titusebbecke/Documents/Work/Helmholtz/2020/Experiments/2003_Hiri_VueBootstrap/hzi_vis_03/public/src/assets", plugin_name))
    metadata['filename'] = plugin_name
    print('yeeet')
    db_plugin_entry_id = db.plugins.insert_one(metadata).inserted_id
    print('ahhh')
    if metadata['db_entry_id'] == '':
        db_entry = {}
        db_entry['plugins_id'] = [db_plugin_entry_id]
        print('heree')
        db_entry_id = db.visualizations.insert_one(db_entry).inserted_id
        print('db_entry_id empty url:', db_entry_id)
    else:
        db_entry = db.visualizations.find_one({"_id": ObjectId(metadata['db_entry_id'])}, {'_id': False})
        plugins_id = db_entry['plugins_id']
        plugins_id.append(db_plugin_entry_id)
        vis_links = visualize.route(db.plugins, pd.DataFrame.from_dict(db_entry['transformed_dataframe']), db_entry['cat_amount'], plugins_id) # CHANGE: Right now every new visualization creates a new MongoDB entry
        db.visualizations.update_one({'_id': ObjectId(metadata['db_entry_id'])}, {'$push': {'plugins_id': db_plugin_entry_id}, '$set': {'vis_links': vis_links}})
        db_entry_id = db_entry['_id']
        print('db_entry_id filled id: ', db_entry_id)
    print('db_plugins_id: ', db_plugin_entry_id)
    return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")

@app.route('/config', methods=['GET', 'POST'])
def respond_config():
    print('responding...')
    if request.form['url'] != 'undefined':
        # import bson
        # from pymongo import MongoClient
        db_entry_id = ObjectId(loads(request.form['url']))
        print('Object_ID: ', db_entry_id)
        db_entry = db.visualizations.find_one({"_id": db_entry_id})
        # print(len(bson.BSON.encode(db_entry)))
        db_entry['_id'] = str(db_entry['_id'])
        db_entry['plugins'] = [plugin for plugin in db.plugins.find({ '_id' : { '$in' : db_entry['plugins_id'] } })]
        return Response(dumps({'db_entry': db_entry}), mimetype="application/json")
    else:
        print('undefined')
        import copy
        db_entry = copy.deepcopy(DB_ENTRY_MOCKUP)
        db_entry['plugins'] = [plugin for plugin in db.plugins.find({ '_id' : { '$in' : db_entry['plugins_id'] } })]
        print(db_entry)
        return Response(dumps({'db_entry': db_entry}), mimetype="application/json")

@app.route('/upload', methods=['GET', 'POST'])
def add_matrix():
    metadata = json.loads(request.form['form'])
    source, extension = upload_file(request, ALLOWED_EXTENSIONS_MATRIX, metadata)
    db_entry_id = process_file.add_matrix(source, metadata, extension, db, PRE_CONFIGURED_PLUGINS)
    return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")

def respond_data(label, payload):
    response_object = {'status': 'success'}
    response_object[label] = payload
    return response_object

def upload_file(request, extension_whitelist, metadata):
    if 'file' in request.files:
        file = request.files['file']
        # If user does not select file, browser also submit an empty part without filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, extension_whitelist):
            print('true')
            extension = os.path.splitext(file.filename)[1]
        print(file)
        return file, extension
    elif metadata['source']['text'] != "null": # If data is pasted text with "Text" as source
        return metadata['source']['text'], "string"
    return "failure"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/matrix/<matrix_id>', methods=['GET', 'POST'])
def remove_matrix(matrix_id):
    metadata = json.loads(request.form['form'])
    print('###### metadata: ', metadata)
    db_entry_id = process_file.remove_matrix(DB_ENTRY_MOCKUP, metadata, db, matrix_id)
    return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")

def make_preview(input_file, extension, dataList, remove_id):
    MATRIX.clear()
    MATRICES, DATAFRAME, db_data_id = process_file.process_upload(input_file, extension.lower(), dataList, remove_id)
    for i in range(len(MATRICES)):
        MATRIX.append(MATRICES[i])
    return DATAFRAME

print('ran')
client.close()
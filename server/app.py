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
UPLOAD_FOLDER = '/static'  # NOTE: Change this to /uploads in production
ALLOWED_EXTENSIONS_MATRIX = {'txt', 'xlsx', 'csv'}
ALLOWED_EXTENSIONS_ICON = {'svg', 'png', 'jpg', 'jpeg', 'gif'}
PRE_CONFIGURED_PLUGINS = [ObjectId('5ed6374fdaf88ae74e38f105'), ObjectId('5f2049b2fda27751b4c96def')]
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

ERROR_MESSAGES = {
    'export_error': {
        'expected': {
            'type': 'Export Error',
            'message': 'The dataframe could not be converted. Please try to change the download type or check your source data.'
        },
        'unexpected': {
            'type': 'Unexpected Export Error',
            'message': 'An unexpected export error has occured. The file cannot be downloaded.'
        }
    },
    'query_error': {
        'expected': {
            'type': 'Filter Error',
            'message': 'The dataframe could not be filtered. Please verify your queries.'
        },
        'unexpected': {
            'type': 'Unexpected Filter Error',
            'message': 'An unexpected filter error has occured.'
        }
    },
    'locking_error': {
        'expected': {
            'type': 'Locking Error',
            'message': "The config could not be locked, because it's corrupted or offline. Please secure your data by downloading it."
        },
        'unexpected': {
            'type': 'Unexpected Locking Error',
            'message': 'An unexpected locking error has occured. The config could not saved. Please secure your data by downloading it.'
        }
    },
    'visualization_error': {
        'expected': {
            'type': 'Visualization Error',
            'message': "The visualization couldn't be initialized because it is either offline or your dataframe is unsupported. Please try a different table."
        },
        'unexpected': {
            'type': 'Unexpected Visualization Error',
            'message': 'An unexpected visualization error has occured.'
        }
    },
    'config_error': {
        'expected': {
            'type': 'Config Error',
            'message': "The config could not be loaded, because it's corrupted or offline. Please try to go back to the homepage."
        },
        'unexpected': {
            'type': 'Unexpected Config Error',
            'message': 'An unexpected error has occured while loading the config.'
        }
    },
    'upload_error': {
        'expected': {
            'type': 'Upload Error',
            'message': "The dataframe could not be uploaded or merged. Try to adjust your data or change the slot."
        },
        'unexpected': {
            'type': 'Unexpected Upload Error',
            'message': 'An unexpected error has occured while uploading the data.'
        }
    },
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
CORS(app, resources={r'/*': {'origins': '*'}})  # enable CORS
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(threaded=True)


def allowed_file(filename, extension_whitelist):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extension_whitelist

# @app.route('/',methods = ['GET','POST'])
# def helloWorld():
#     print('hello world')
#     return "Hello world!"


@app.route('/export', methods=['POST'])
def export_df():
    try:
        # import pandas as pd
        # export_form = json.loads(request.form['export_form'])
        # url = json.loads(request.form['url'])
        # db_entry = db.visualizations.find_one(
        #     {"_id": ObjectId(url)}, {'_id': False})
        # dataframe_dict = {}
        # try:
        #     df_filtered = pd.DataFrame.from_dict(
        #         db_entry['filtered_dataframe'])
        #     dataframe_dict["filtered"] = {}
        #     dataframe_dict["filtered"]["df"] = df_filtered
        #     dataframe_dict["filtered"]["name"] = "Filtered Data"
        # except KeyError:
        #     pass
        # dataframe_dict["unfiltered"] = {}
        # dataframe_dict["unfiltered"]["df"] = pd.DataFrame.from_dict(
        #     db_entry['transformed_dataframe'])
        # dataframe_dict["unfiltered"]["name"] = "Source Data"
        # if export_form["file_type"] == 'excel':
        #     res = df_to_excel(dataframe_dict)
        # elif export_form["file_type"] == 'csv':
        #     res = df_to_csv(dataframe_dict, export_form['csv_seperator'])
        # return res
        return respond_error(ERROR_MESSAGES["export_error"]["expected"]["type"], ERROR_MESSAGES["export_error"]["expected"]["message"])
    except ValueError:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['export_error']['expected']['type'], ERROR_MESSAGES['export_error']['expected']['message'])
    else:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['export_error']['unexpected']['type'], ERROR_MESSAGES['export_error']['unexpected']['message'])


def df_to_excel(dataframe_dict):
    from io import BytesIO
    import pandas as pd
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    # Load the filtered, and unfiltered dataframe as excel sheets.
    for dataframe_parent in dataframe_dict:
        dataframe_dict[dataframe_parent]["df"].to_excel(
            writer, sheet_name=dataframe_dict[dataframe_parent]["name"], index=False)
    writer.close()
    output.seek(0)
    return Response(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-disposition": "attachment; filename=filename.xlsx"})


def df_to_csv(dataframe_dict, seperator):
    # CSV doesn't support multi-sheets, so only one dataframe can be exported.
    try:
        df = dataframe_dict["filtered"]["df"]
    except KeyError:
        df = dataframe_dict["unfiltered"]["df"]
    return Response(df.to_csv(sep=seperator, index=False, encoding='utf-8'), mimetype="text/csv", headers={"Content-disposition": "attachment; filename=filename.csv"})


def upload_db_entry(db_entry, mongo_update, url):
    if 'locked' in db_entry and db_entry['locked'] == True:
        db_entry['locked'] = False
        db_entry_id = db.visualizations.insert_one(db_entry).inserted_id
    else:
        db_entry_id = ObjectId(url)
        db.visualizations.update_one({'_id': db_entry_id}, mongo_update)
    return db_entry_id


@app.route('/query', methods=['POST'])
def search_query():
    try:
        import filter_dataframe
        import pandas as pd
        query = json.loads(request.form['query'])
        url = json.loads(request.form['url'])
        db_entry = db.visualizations.find_one(
            {"_id": ObjectId(url)}, {'_id': False})
        df = pd.DataFrame.from_dict(db_entry['transformed_dataframe'])
        print('query: ', query)
        filtered_df = filter_dataframe.main(query, df)
        mongo_update = {
            '$set': {
                'filtered_dataframe': filtered_df.to_dict('records'),
                'vis_links': [],
                'query': query
            }
        }
        db_entry_id = upload_db_entry(db_entry, mongo_update, url)
        return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")
    except KeyError:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['query_error']['expected']['type'], ERROR_MESSAGES['query_error']['expected']['message'])
    else:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['query_error']['unexpected']['type'], ERROR_MESSAGES['query_error']['unexpected']['message'])


@app.route('/locked', methods=['POST'])
def lock_session():
    try:
        from pymongo import MongoClient
        url = json.loads(request.form['url'])
        print('URL: ', url)
        db.visualizations.update_one({'_id': ObjectId(url)}, {
            '$set': {'locked': True}})
        return "success"
    except KeyError:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['locking_error']['expected']['type'], ERROR_MESSAGES['locking_error']['expected']['message'])
    else:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['locking_error']['unexpected']['type'], ERROR_MESSAGES['locking_error']['unexpected']['message'])


@app.route('/visualization', methods=['POST'])
def make_vis_link():
    try:
        import pandas as pd
        plugin = json.loads(request.form['plugin'])
        url = json.loads(request.form['url'])
        print('url: ', url, 'plugin: ', plugin)
        db_entry = db.visualizations.find_one(
            {"_id": ObjectId(url)}, {'_id': False})
        # CHANGE: Right now every new visualization creates a new MongoDB entry
        vis_link = visualize.route(db.plugins, pd.DataFrame.from_dict(
            db_entry['transformed_dataframe']), db_entry['cat_amount'], plugin)
        db.visualizations.update_one({'_id': ObjectId(url)}, {
            '$push': {'vis_links': vis_link}})
        print(vis_link)
        print('########')
        print(Response({'vis_link': vis_link}))
        return Response(dumps({'vis_link': vis_link}), mimetype="application/json")
    except (IndexError, TypeError):
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['visualization_error']['expected']['type'], ERROR_MESSAGES['visualization_error']['expected']['message'])
    else:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['visualization_error']['unexpected']['type'], ERROR_MESSAGES['visualization_error']['unexpected']['message'])

@app.route('/plugins', methods=['POST'])
def add_plugin():
    import pandas as pd
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    metadata = json.loads(request.form['form'])
    source, extension = upload_file(request, ALLOWED_EXTENSIONS_ICON, metadata)
    plugin_name = secure_filename(source.filename)
    source.save(os.path.join(
        "/Users/titusebbecke/Documents/Work/Helmholtz/2020/Experiments/2003_Hiri_VueBootstrap/hzi_vis_03/public/src/assets", plugin_name))
    metadata['filename'] = plugin_name
    db_plugin_entry_id = db.plugins.insert_one(metadata).inserted_id
    if metadata['db_entry_id'] == '':
        import copy
        db_entry = copy.deepcopy(DB_ENTRY_MOCKUP)
        db_entry['plugins_id'].append(db_plugin_entry_id)
        db_entry['locked'] = False
        db_entry_id = db.visualizations.insert_one(db_entry).inserted_id
        print('db_entry_id empty url:', db_entry_id)
    else:
        db_entry = db.visualizations.find_one(
            {"_id": ObjectId(metadata['db_entry_id'])}, {'_id': False})
        plugins_id = db_entry['plugins_id']
        plugins_id.append(db_plugin_entry_id)
        db.visualizations.update_one({'_id': ObjectId(metadata['db_entry_id'])}, {
                                     '$push': {'plugins_id': db_plugin_entry_id}})
        print("metadata['db_entry']", metadata['db_entry_id'])
        db_entry_id = ObjectId(metadata['db_entry_id'])
        print('db_entry_id filled id: ', db_entry_id)
    print('db_plugins_id: ', db_plugin_entry_id)
    return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")

@app.route('/datasets', methods=['GET'])
def respond_datasets():
    db_dataset

@app.route('/config', methods=['GET', 'POST'])
def respond_config():
    print('responding...')
    try:
        if request.form['url'] != 'undefined':
            # import bson
            # from pymongo import MongoClient
            db_entry_id = ObjectId(loads(request.form['url']))
            print('Object_ID: ', db_entry_id)
            db_entry = db.visualizations.find_one({"_id": db_entry_id})
            # print(len(bson.BSON.encode(db_entry)))
            db_entry['_id'] = str(db_entry['_id'])
            db_entry['plugins'] = [plugin for plugin in db.plugins.find(
                {'_id': {'$in': db_entry['plugins_id']}})]
            return Response(dumps({'db_entry': db_entry}), mimetype="application/json")
        else:
            print('undefined')
            import copy
            db_entry = copy.deepcopy(DB_ENTRY_MOCKUP)

            db_entry['plugins'] = [plugin for plugin in db.plugins.find(
                {'_id': {'$in': db_entry['plugins_id']}})]
            print(db_entry)
            return Response(dumps({'db_entry': db_entry}), mimetype="application/json")
    except KeyError:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['config_error']['expected']['type'], ERROR_MESSAGES['config_error']['expected']['message'])
    else:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['config_error']['unexpected']['type'], ERROR_MESSAGES['config_error']['unexpected']['message'])


def respond_error(error_type, error_message):
    return Response(dumps({'error_type': error_type, 'error_message': error_message}), mimetype="application/json")


@app.route('/upload', methods=['GET', 'POST'])
def add_matrix():
    try:
        metadata = json.loads(request.form['form'])
        print('metadata: ', metadata)
        source, extension = upload_file(
            request, ALLOWED_EXTENSIONS_MATRIX, metadata)
        db_entry_id = process_file.add_matrix(
            source, metadata, extension, db, PRE_CONFIGURED_PLUGINS)
        return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")
    except ValueError:
        print('###### ERROR')
        return respond_error(ERROR_MESSAGES['upload_error']['expected']['type'], ERROR_MESSAGES['upload_error']['expected']['message'])
    else:
        print('ERROR')
        return respond_error(ERROR_MESSAGES['upload_error']['unexpected']['type'], ERROR_MESSAGES['upload_error']['unexpected']['message'])


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
    # If data is pasted text with "Text" as source
    elif metadata['source']['text'] != "null":
        return metadata['source']['text'], "string"
    return "failure"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/matrix/<matrix_id>', methods=['GET', 'POST'])
def remove_matrix(matrix_id):
    metadata = json.loads(request.form['form'])
    print('###### metadata: ', metadata)
    db_entry_id = process_file.remove_matrix(
        DB_ENTRY_MOCKUP, metadata, db, matrix_id)
    return Response(dumps({'db_entry_id': db_entry_id}), mimetype="application/json")


def make_preview(input_file, extension, dataList, remove_id):
    MATRIX.clear()
    MATRICES, DATAFRAME, db_data_id = process_file.process_upload(
        input_file, extension.lower(), dataList, remove_id)
    for i in range(len(MATRICES)):
        MATRIX.append(MATRICES[i])
    return DATAFRAME


print('ran')
client.close()

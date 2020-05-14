import uuid
import pandas as pd

max_preview_rows = 12
max_preview_columns = 8
max_y = 1
active_matrices = [[]]

def convert_to_df(input_file, index, extension):
    import pandas as pd
    if extension == ".xlsx":
        df = pd.read_excel(input_file)
    elif extension == ".csv":
        df = pd.read_csv(input_file, sep=';')
    elif extension == ".txt":
        df = pd.read_csv(input_file, sep='\t')
    else:
        print("Error: No valid extension. Please upload .xlsx (Excel), .csv, or .txt (TSV).")
        return "Error"
    # df = df.set_index(index)
    return df

def main(input_file, metadata, extension, collection, vis_plugin):
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    import visualize
    # db.visualizations.find_one({"_id": db_entry_id})
    # db_updated_document = db.update_one({'_id': id}, {'$push': {'dataframes': df}})
    df = convert_to_df(input_file, metadata['index'], extension)
    if metadata['db_entry_id'] != '':
        db_entry = collection.find_one({"_id": ObjectId(metadata['db_entry_id'])}, {'_id': False})
        df_merged = pd.merge(pd.DataFrame.from_dict(db_entry['transformed_dataframe']), df, how='outer')
        df_merged.fillna(0, inplace=True)
        db_entry['transformed_dataframe'] = df_merged.to_dict('records')
        print('###############', db_entry['transformed_dataframe'])
        print('####')
    else:
        db_entry = {}
        db_entry['active_matrices'] = [[]]
        db_entry['transformed_dataframe'] = df.to_dict('records')
        db_entry['dataframes'] = []
    active_matrices, added_axis = make_active_matrix(metadata, df, db_entry['active_matrices'])
    db_entry['dataframes'].append(df.to_dict('records'))
    db_entry['active_matrices'] = active_matrices
    db_entry['preview_matrices'] = make_preview_matrices(active_matrices)
    db_entry['vis_link'] = visualize.route(vis_plugin, pd.DataFrame.from_dict(db_entry['transformed_dataframe'])) # CHANGE: Right now every new visualization creates a new MongoDB entry
    db_entry_id = collection.insert_one(db_entry).inserted_id
    return db_entry_id


    # db_updated_document = update_one({'_id': id}, {'$push': {'dataframes': dataframes}})

# def process_upload(input_file, extension, metadata, remove_id):
#     global active_matrices
#     global merged_df
#     active_matrices, df, added_axis = make_active_matrix(input_file, extension, metadata, active_matrices, remove_id)
#     if len(active_matrices[0])>1:
#         merged_df = merge_dataframes(merged_df, df, metadata['title'], added_axis)
#     else:
#         merged_df = df
#     db_data_id = save_df_mongo(merged_df, metadata)
#     matrices = make_matrices(active_matrices)
#     return matrices, merged_df, db_data_id

# def merge_dataframes(merged_df, df, title, added_axis):
#     print("added_axis: ", added_axis)
#     #merged_dataframe = pd.merge(merged_df, df, on=['GeneID', 'Locus_tag', 'Strand', 'Start', 'End'])
#     #merged_dataframe = pd.concat([merged_df, df], axis=added_axis, join='outer', sort=False)
#     merged_dataframe = pd.merge(merged_df, df, how='outer') # Replace same Column+Row, append different ones
#     #merged_dataframe = pd.concat([merged_df, df], axis=added_axis, join='outer', ignore_index=True, keys=title, levels=None, names=None, verify_integrity=False, copy=True)
#     print('df: ', merged_dataframe)
#     merged_dataframe.to_csv("inspect.txt", sep='\t', index=False)
#     print('done')
#     return merged_dataframe


def make_active_matrix(metadata, df, active_matrices):
    added_matrix = make_single_matrix(metadata['x'],metadata['y'],max_preview_columns,max_preview_rows,metadata['title'],True)
    added_axis = 1
    if added_matrix['y']-1>len(active_matrices): # If new matrix is below current matrices (y-axis)
        active_matrices.append([])
        added_axis = 0
    elif added_matrix['y']<=1: # If new matrix is above current matrices (y-axis)
        active_matrices.insert(0, [])
        added_matrix['y']=2
        added_axis = 0
    if df.shape[0]<max_preview_rows:
        added_matrix['height'] = df.shape[0]
    if df.shape[1]<max_preview_columns:
        added_matrix['width'] = df.shape[1]
    active_matrices[added_matrix['y']-2].insert(added_matrix['x']-2, added_matrix)
    for matrixY in range(len(active_matrices)):
        for matrixX in range(len(active_matrices[matrixY])):
            active_matrices[matrixY][matrixX]['x'] = matrixX+2
            active_matrices[matrixY][matrixX]['y'] = matrixY+2
    return active_matrices, added_axis

def make_preview_matrices(active_matrices):
    import copy
    preview_matrices = [] # flush all preview_matrices to rebuild it later. Bad perfomance < more readable algorithm
    flattened_active_matrices = copy.deepcopy(sum(active_matrices, []))
    print("active_matrices: ", active_matrices)
    for matrix in flattened_active_matrices:
        preview_matrices.append(matrix)
        print('preview_matrices, after flattened injection: ', preview_matrices)
    for topMatrix in range(len(active_matrices[0])):
        preview_matrices.append(make_single_matrix(topMatrix+2, 1, active_matrices[0][topMatrix]['width'], 2, "", False))
    for bottomMatrix in range(len(active_matrices[0])):
        preview_matrices.append(make_single_matrix(bottomMatrix+2, len(active_matrices)+2, active_matrices[len(active_matrices)-1][bottomMatrix]['width'], 2, "", False))
    for leftMatrix in range(len(active_matrices)):
        preview_matrices.append(make_single_matrix(1, leftMatrix+2, 2, active_matrices[leftMatrix][0]['height'], "", False))
    for rightMatrix in range(len(active_matrices)):
        preview_matrices.append(make_single_matrix(len(active_matrices[0])+2, rightMatrix+2, 2, active_matrices[rightMatrix][len(active_matrices[0])-1]['height'], "", False))
    return preview_matrices

def make_single_matrix(x, y, width, height, title, active):
    ADD_MATRIX = {
        'title': title,
        'id': uuid.uuid4().hex,
        "width": width,
        'height': height,
        'x': x,
        'y': y,
        'isActive': active
    }
    return ADD_MATRIX

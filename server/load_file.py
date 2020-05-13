import uuid
import pandas as pd

max_preview_rows = 12
max_preview_columns = 8
matrices = []
max_y = 1
active_matrices = [[]]

def save_df_mongo(dataframe, metadata):
    from pymongo import MongoClient
    import pandas as pd
    data_dict = {}
    data_dict['metadata'] = metadata
    data_dict['dataframe'] = dataframe.to_dict('records')
    
    client = MongoClient()
    db = client.projectname
    visualizations = db.visualizations
    
    data_id = visualizations.insert(data_dict)
    client.close()
    temp_data = db.visualizations.find_one({"_id": data_id})
    print(data_id)
    return data_id

def process_upload(input_file, extension, metadata, remove_id):
    global active_matrices
    global merged_df
    active_matrices, df, added_axis = make_active_matrix(input_file, extension, metadata, active_matrices, remove_id)
    df.set_index('GeneID')
    if len(active_matrices[0])>1:
        merged_df = merge_dataframes(merged_df, df, metadata['title'], added_axis)
    else:
        merged_df = df
    save_df_mongo(merged_df, metadata)
    matrices = make_matrices(active_matrices)
    return matrices, merged_df

def merge_dataframes(merged_df, df, title, added_axis):
    print("added_axis: ", added_axis)
    #merged_dataframe = pd.merge(merged_df, df, on=['GeneID', 'Locus_tag', 'Strand', 'Start', 'End'])
    #merged_dataframe = pd.concat([merged_df, df], axis=added_axis, join='outer', sort=False)
    merged_dataframe = pd.merge(merged_df, df, how='outer') # Replace same Column+Row, append different ones
    #merged_dataframe = pd.concat([merged_df, df], axis=added_axis, join='outer', ignore_index=True, keys=title, levels=None, names=None, verify_integrity=False, copy=True)
    print('df: ', merged_dataframe)
    merged_dataframe.to_csv("inspect.txt", sep='\t', index=False)
    print('done')
    return merged_dataframe


def make_active_matrix(input_file, extension, metadata, active_matrices, remove_id):
    if input_file != False:
        if extension == ".xlsx":
            df = pd.read_excel(input_file)
        elif extension == ".csv":
            df = pd.read_csv(input_file, sep=';')
        elif extension == ".txt":
            df = pd.read_csv(input_file, sep='\t')
        else:
            print("Error: No valid extension. Please upload .xlsx (Excel), .csv, or .txt (TSV).")
            return "Error"
        # df = df.set_index('GeneID')
        print('df: ', df)
        MATRIX = make_single_matrix(metadata['x'],metadata['y'],max_preview_columns,max_preview_rows,metadata['title'],True, df)
        added_axis = 1
        if MATRIX['y']-1>len(active_matrices): # If new matrix is below current matrices (y-axis)
            active_matrices.append([])
            added_axis = 0
        elif MATRIX['y']<=1: # If new matrix is above current matrices (y-axis)
            active_matrices.insert(0, [])
            MATRIX['y']=2
            added_axis = 0
        if df.shape[0]<max_preview_rows:
            MATRIX['height'] = df.shape[0]
        if df.shape[1]<max_preview_columns:
            MATRIX['width'] = df.shape[1]
        active_matrices[MATRIX['y']-2].insert(MATRIX['x']-2, MATRIX)
    else:
        active_matrices = [[i for i in nested if i['id'] != remove_id] for nested in active_matrices] # remove entries matching the remove_id
        active_matrices = [j for j in active_matrices if j != []] # remove empty subarrays
    for matrixY in range(len(active_matrices)):
        for matrixX in range(len(active_matrices[matrixY])):
            active_matrices[matrixY][matrixX]['x'] = matrixX+2
            active_matrices[matrixY][matrixX]['y'] = matrixY+2
    return active_matrices, df, added_axis

def make_matrices(active_matrices):
    import copy
    matrices.clear() # flush all matrices to rebuild it later. Bad perfomance < more readable algorithm
    flattened_active_matrices = copy.deepcopy(sum(active_matrices, []))
    print("active_matrices: ", active_matrices)
    for dict in flattened_active_matrices:
        dict.pop('dataframe')
    for matrix in flattened_active_matrices:
        matrices.append(matrix)
    for topMatrix in range(len(active_matrices[0])):
        matrices.append(make_single_matrix(topMatrix+2, 1, active_matrices[0][topMatrix]['width'], 2, "", False, False))
    for bottomMatrix in range(len(active_matrices[0])):
        matrices.append(make_single_matrix(bottomMatrix+2, len(active_matrices)+2, active_matrices[len(active_matrices)-1][bottomMatrix]['width'], 2, "", False, False))
    for leftMatrix in range(len(active_matrices)):
        matrices.append(make_single_matrix(1, leftMatrix+2, 2, active_matrices[leftMatrix][0]['height'], "", False, False))
    for rightMatrix in range(len(active_matrices)):
        matrices.append(make_single_matrix(len(active_matrices[0])+2, rightMatrix+2, 2, active_matrices[rightMatrix][len(active_matrices[0])-1]['height'], "", False, False))
    return matrices

def make_single_matrix(x, y, width, height, title, active, df):
    ADD_MATRIX = {
        'title': title,
        'id': uuid.uuid4().hex,
        "width": width,
        'height': height,
        'x': x,
        'y': y,
        'isActive': active,
        'dataframe': df
    }
    return ADD_MATRIX
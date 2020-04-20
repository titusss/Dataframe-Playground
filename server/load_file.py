import uuid
import copy

max_preview_rows = 12
max_preview_columns = 8
matrices = []
max_y = 1
active_matrices = [[]]

def process_upload(input_file, extension, metadata, remove_id):
    global active_matrices
    active_matrices = make_active_matrix(input_file, extension, metadata, active_matrices, remove_id)
    matrices = make_matrices(active_matrices)
    return matrices

def make_active_matrix(input_file, extension, metadata, active_matrices, remove_id):
    if input_file != False:
        import pandas as pd
        if extension == ".xlsx":
            df = pd.read_excel(input_file)
        elif extension == ".csv":
            df = pd.read_csv(input_file)
        elif extension == ".txt":
            df = pd.read_csv(input_file, sep='\t')
        else:
            print("Error: No valid extension. Please upload .xlsx (Excel), .csv, or .txt (TSV).")
            return
        MATRIX = make_single_matrix(metadata['x'],metadata['y'],max_preview_columns,max_preview_rows,metadata['title'],True)
        if MATRIX['y']-1>len(active_matrices):
            active_matrices.append([])
        elif MATRIX['y']<=1:
            active_matrices.insert(0, [])
            MATRIX['y']=2
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
    return active_matrices

def make_matrices(active_matrices):
    matrices.clear() # flush all matrices to rebuild it later. Bad perfomance < more readable algorithm
    flattened_active_matrices = sum(active_matrices, [])
    for matrix in flattened_active_matrices:
        matrices.append(matrix)
    for topMatrix in range(len(active_matrices[0])):
        matrices.append(make_single_matrix(topMatrix+2, 1, active_matrices[0][topMatrix]['width'], 2, "", False))
    for bottomMatrix in range(len(active_matrices[0])):
        matrices.append(make_single_matrix(bottomMatrix+2, len(active_matrices)+2, active_matrices[len(active_matrices)-1][bottomMatrix]['width'], 2, "", False))
    for leftMatrix in range(len(active_matrices)):
        matrices.append(make_single_matrix(1, leftMatrix+2, 2, active_matrices[leftMatrix][0]['height'], "", False))
    for rightMatrix in range(len(active_matrices)):
        matrices.append(make_single_matrix(len(active_matrices[0])+2, rightMatrix+2, 2, active_matrices[rightMatrix][len(active_matrices[0])-1]['height'], "", False))
    return matrices

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
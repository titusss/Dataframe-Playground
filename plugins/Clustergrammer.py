def main(df):
    import requests
    file_path = csv_to_tsv(df) # Define the path to the file you want to visualize.
    upload_url = "http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/" # Define the path to the visualizing sertver endpoint.
    response = requests.post(upload_url, files={'file': open(file_path, 'rb')})
    print(response.text)
    vis_link = response.text
    return vis_link

def csv_to_tsv(df):
    import pandas as pd
    import copy
    dataframe = copy.deepcopy(df)
    file_path = "uploads/output_matrix.txt"

    # Append category title string before values for all cat columns.
    # dataframe[dataframe.columns[0:cat_amount]] = dataframe.columns[0:cat_amount] + \
    #     ': ' + dataframe[dataframe.columns[0:cat_amount]].astype(str)
    # Remove the category titles from first row.
    categories = df.select_dtypes(exclude=[np.number]).columns # Get all columns that are non numerics
    value_columns = [x for x in list(df.columns) if x not in categories] # Get all columns that are not category columns
    print('categoris: ', value_columns)
    print("categories: ", categories)
    dataframe = dataframe[[categories += value_columns]] # Put all categories column to the beginning of the dataframe.
    print(dataframe)
    if len(categories) > 0:
        for category in categories:
            dataframe[category] = dataframe.category.name + ': ' + dataframe[category].astype(str)
            dataframe = dataframe.rename(columns={category: ''})
    else:
        dataframe.columns[0] = dataframe.columns[0].name + ': ' + dataframe.columns[0].astype(str)
        dataframe = dataframe.rename(columns={dataframe.columns[0]: ''})
    print(dataframe)
    # Export the data frame as tab-seperated .txt.
    dataframe.to_csv(file_path, sep='\t', index=False)
    print('Output file has been generated and saved.')
    return file_path
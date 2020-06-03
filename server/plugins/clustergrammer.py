def main(df, cat_amount):
    import requests
    file_path = csv_to_tsv(df, cat_amount) # Define the path to the file you want to visualize.
    upload_url = "http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/" # Define the path to the visualizing sertver endpoint.
    response = requests.post(upload_url, files={'file': open(file_path, 'rb')})
    print(response.text)
    vis_link = response.text
    return vis_link

def csv_to_tsv(df, cat_amount):
    import pandas as pd
    import copy
    dataframe = copy.deepcopy(df)
    file_path = "uploads/output_matrix.txt"
    print('cat_aount: ', cat_amount)
    # Append category title string before values for all cat columns.
    dataframe[dataframe.columns[0:cat_amount]] = dataframe.columns[0:cat_amount] + \
        ': ' + dataframe[dataframe.columns[0:cat_amount]].astype(str)
    # Remove the category titles from first row.
    for i in range(cat_amount):
        dataframe = dataframe.rename(columns={dataframe.columns[i]: ''})
    # Export the data frame as tab-seperated .txt.
    dataframe.to_csv(file_path, sep='\t', index=False)
    print('Output file has been generated and saved.')
    return file_path
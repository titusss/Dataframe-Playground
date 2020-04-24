def main(df):
    file_path = csv_to_tsv(df, 5) # Define the path to the file you want to visualize.
    upload_url = "http://amp.pharm.mssm.edu/clustergrammer/matrix_upload/" # Define the path to the visualizing sertver endpoint.
    print(upload_url, file_path)
    return upload_url, file_path

def csv_to_tsv(df, cat_amount):
    import pandas as pd
    file_path = "uploads/output_matrix.txt"
    # Append category title string before values for all cat columns.
    df[df.columns[0:cat_amount]] = df.columns[0:cat_amount] + \
        ': ' + df[df.columns[0:cat_amount]].astype(str)
    # Remove the category titles from first row.
    for i in range(cat_amount):
        df = df.rename(columns={df.columns[i]: ''})
    # Export the data frame as tab-seperated .txt.
    df.to_csv(file_path, sep='\t', index=False)
    print('Output file has been generated and saved.')
    return file_path
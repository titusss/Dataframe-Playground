# Module for converting .csv to tab-seperated .txt
def csv_to_tsv(input_file, cat_amount):
    import pandas as pd
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
    from clustergrammer import Network
    # This creates a network and loads it into a file.
    net = Network()
    net.load_file(MatrixName + '.txt')
    net.cluster(dist_type='cos', views=['N_row_sum', 'N_row_var'], dendro=True,
                sim_mat=True, filter_sim=0.1, calc_cat_pval=False, enrichrgram=False, run_clustering=True)
    # write jsons for front-end visualizations
    net.write_json_to_file('viz', 'json/mult_view.json', 'indent')
    net.write_json_to_file('sim_row', 'json/mult_view_sim_row.json', 'no-indent')
    net.write_json_to_file('sim_col', 'json/mult_view_sim_col.json', 'no-indent')

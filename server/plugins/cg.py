def status(df):
    print("Succesfully loaded this module!")
    import plugins.cg_make_matrix as cg
    cg.csv_to_tsv(df, 5)
    cg.make_json('output_matrix.txt')

def save_df_mongo(df, metadata):
    from pymongo import MongoClient
    import pandas as pd
    data_dict = {}
    data_dict['metadata'] = metadata
    data_dict['dataframes'] = df.to_dict('records')
    client = MongoClient()
    db = client.projectname
    visualizations = db.visualizations
    db_data_id = visualizations.insert(data_dict)
    client.close()
    # temp_data = db.visualizations.find_one({"_id": db_data_id})
    return db_data_id
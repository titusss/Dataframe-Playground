def main(df):
    import uuid
    import cufflinks as cf
    import pandas as pd
    import numpy as np
    categories = list(df.select_dtypes(exclude=[np.number]).columns) # Get all columns that are non numeric
    df.set_index(categories, inplace=True)

    print(df)
    # upload_url = df.iplot(kind='heatmap', filename=str(uuid.uuid4()), asUrl=True, colorscale='RdBu')
    upload_url = df.iplot(kind='bar', barmode='stack', filename=str(uuid.uuid4()), asUrl=True, colorscale='RdBu')
    print(upload_url)


    return upload_url
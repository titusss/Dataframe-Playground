def main(df, cat_amount):
    import uuid
    import cufflinks as cf
    import pandas as pd
    if cat_amount>0:
        df.set_index(list(df.columns[:cat_amount]), inplace=True)
    print(df)
    upload_url = df.iplot(kind='heatmap', filename=str(uuid.uuid4()), asUrl=True, colorscale='RdBu')
    print(upload_url)


    return upload_url
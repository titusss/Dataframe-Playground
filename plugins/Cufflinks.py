def main(df):
    import uuid
    import cufflinks as cf
    import pandas as pd
    import numpy as np
    import chart_studio
    import os
    chart_studio.tools.set_credentials_file(username='tebbecke', api_key=os.environ.get("CHART_STUDIO_API_KEY"))
    categories = list(df.select_dtypes(exclude=[np.number]).columns) # Get all columns that are non numeric
    df.set_index(categories, inplace=True)
    # upload_url = df.iplot(kind='heatmap', filename=str(uuid.uuid4()), asUrl=True, colorscale='RdBu')
    upload_url = df.iplot(kind='bar', barmode='stack', filename=str(uuid.uuid4()), asUrl=True, colorscale='RdBu')

    return upload_url
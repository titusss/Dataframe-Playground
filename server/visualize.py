# This is the main point for visualizations.
# Parse all relevant dataframes to this module and decide what plugin to use with route().

def route(vis_plugin, df, cat_amount):
    import importlib
    import requests
    vis = importlib.import_module("plugins.{}".format(vis_plugin))
    upload_url, file_path = vis.main(df, cat_amount)
    response = requests.post(upload_url, files={'file': open(file_path, 'rb')})
    print(response.text)
    vis_link = response.text
    return vis_link

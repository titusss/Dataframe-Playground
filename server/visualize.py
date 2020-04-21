def route(vis_plugin, df):
    import importlib
    vis = importlib.import_module("plugins.{}".format(vis_plugin))
    print(df)
    vis.status(df)
    return

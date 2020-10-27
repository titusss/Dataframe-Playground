# This is the main point for visualizations.
# Parse all relevant dataframes to this module and decide what plugin to use with route().

def route(collection, df, plugin, db_entry_id):
    import importlib
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    plugin_module = importlib.import_module("plugins.{}".format(plugin['name']))
    visualization = {}
    visualization['plugin_name'] = plugin['name']
    visualization['plugin_id'] = str(plugin['_id']['$oid'])
    visualization['link'] = plugin_module.main({"df":df, "db_entry_id": db_entry_id})
    print('vis_links: ', visualization)
    return visualization
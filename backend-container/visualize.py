# This is the main point for visualizations.
# Parse all relevant dataframes to this module and decide what plugin to use with route().

<<<<<<< HEAD
def route(collection, df, cat_amount, plugin):
    import importlib
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    print(plugin)
=======
def route(collection, df, plugin, db_entry_id):
    import importlib
    from pymongo import MongoClient
    from bson.json_util import ObjectId
>>>>>>> Moved backend to dedicated Container folder.
    plugin_module = importlib.import_module("plugins.{}".format(plugin['name']))
    visualization = {}
    visualization['plugin_name'] = plugin['name']
    visualization['plugin_id'] = str(plugin['_id']['$oid'])
<<<<<<< HEAD
    visualization['link'] = plugin_module.main(df, cat_amount)
=======
    visualization['link'] = plugin_module.main({"df":df, "db_entry_id": db_entry_id})
>>>>>>> Moved backend to dedicated Container folder.
    print('vis_links: ', visualization)
    return visualization
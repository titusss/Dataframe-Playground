# This is the main point for visualizations.
# Parse all relevant dataframes to this module and decide what plugin to use with route().

def route(collection, df, cat_amount, plugins_id):
    import importlib
    from pymongo import MongoClient
    from bson.json_util import ObjectId
    vis_links = []
    print('plugins_id: ', plugins_id)
    for i in range(len(plugins_id)):
        print('i: ', i)
        plugin_entry = collection.find_one({"_id": ObjectId(plugins_id[i])})
        print('plugin_entry: ', plugin_entry)
        plugin = importlib.import_module("plugins.{}".format(plugin_entry['name']))
        entry = {}
        entry['plugin_name'] = plugin_entry['name']
        entry['link'] = plugin.main(df, cat_amount)
        print(entry)
        vis_links.append(entry)
        print('vis_links: ', vis_links)
    return vis_links
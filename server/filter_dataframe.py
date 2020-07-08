import pandas as pd

COMPARISON_OPERATORS = {
    '< less than': '<',
    '> more than': '>',
    '>= more or equal to': '>=',
    '<= less or equal to': '<=',
    '= equal to': '==',
    '!= not': '!='
}

def value_filter(query, df):
    df.set_index(df.columns[0], inplace=True)
    try:
        selection = query['column']
    except KeyError:
        selection = df.columns
    else:
        selection = df.columns
    print(COMPARISON_OPERATORS[query["logical_operator"]["selected"]])
    print(query["value"]["selected"])
    df_filtered = eval('df[df[selection]'+ COMPARISON_OPERATORS[query["logical_operator"]["selected"]] + query["value"]["selected"]+']') # DANGER DANGER DANGER!!! ADD EXCEPTIONS AND WHITELISTS TO EVAL()!!!!
    df_filtered.fillna('undefined', inplace=True)
    df.reset_index(inplace=True)
    print('df_filtered: ', df_filtered)
    return df_filtered

def keyword_filter(query, df, annotation_id):
    import json
    print(query)
    go_name = query['search']['selected']
    with open('static/salmonella_annotations.json') as json_file:
        salmonella_annotations = json.load(json_file)

    df_locus = df[df.columns[0]].tolist()
    # print('df_locus: ', df_locus)
    filtered_locus = []

    for salmonella_locus in salmonella_annotations:
        if salmonella_locus in df_locus:
            if go_name in salmonella_annotations[salmonella_locus][annotation_id]:
                filtered_locus.append(salmonella_locus)
    print('filtered_locus: ', '#', filtered_locus)
    print(df.columns[0])
    df_filtered = df[df[df.columns[0]].isin(filtered_locus)]
    print('######')
    print(df_filtered)
    return df_filtered


def main(query, df):
    for array in query:
        for block in array:
            try:
                print(block['logical_operator'])
                df_filtered = value_filter(block, df)
            except KeyError:
                if block['search']!='':
                    print('###### SEARCH')
                    print('block: ', block)
                    df_filtered = keyword_filter(block, df, "test")
    return df_filtered
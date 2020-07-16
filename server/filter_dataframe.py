import pandas as pd
import numpy as np
import operator
COMPARISON_OPERATORS = {
    '< less than': operator.lt,
    '> more than': operator.gt,
    '>= more or equal to': operator.ge,
    '<= less or equal to': operator.le,
    '= equal to': operator.eq,
    '!= not': operator.ne
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
    print(query)
    for block in query:
        print('block: ', block)
        df = filter_for(block["forms"], df)
    return df


def filter_for(form, df):
    df_numeric = df.select_dtypes(include=[np.number])
    try:
        comparison_operator = COMPARISON_OPERATORS[form["logical_operator"]]
    except KeyError:
        comparison_operator = operator.eq
    if form["filter_area"] == "all columns":
        filter_area = list(df_numeric.columns)
    else:
        filter_area = form["filter_area"]
    try:
        filter_value = float(form["filter_value"])
    except ValueError:
        filter_value = str(form["filter_value"])
    df = df[comparison_operator(df[filter_area].values, filter_value)]
    return df

    
    
    # except KeyError:
    #     filter_annotation = forms["filter_annotation"]
    #     filter_source = "go_name"
    #     filter_value = 


    # df_filtered = eval('df[df[selection]'+ COMPARISON_OPERATORS[forms["logical_operator"]] + forms["value"]["selected"]+']') # DANGER DANGER DANGER!!! ADD EXCEPTIONS AND WHITELISTS TO EVAL()!!!!


# def main(query, df):
#     for array in query:
#         for block in array:
#             try:
#                 print(block['logical_operator'])
#                 df_filtered = value_filter(block, df)
#             except KeyError:
#                 if block['search']!='':
#                     print('###### SEARCH')
#                     print('block: ', block)
#                     df_filtered = keyword_filter(block, df, "test")
#     return df_filtered
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

def main(query, df):
    print(query)
    for block in query:
        block_type = block["properties"]["type"]
        if block_type == "filter":
            df = filter_for(block["forms"], block["properties"], df)
    return df

def filter_for(form, properties, df):
    df_numeric = df.select_dtypes(include=[np.number])
    try:
        comparison_operator = COMPARISON_OPERATORS[form["logical_operator"]]
    except KeyError:
        comparison_operator = operator.eq # If no comparison operator is given, set it to "equal (=)"
    if form["filter_area"] == "all columns":
        filter_area = list(df_numeric.columns)
    else:
        filter_area = form["filter_area"]
    if properties["query"] == "expression":
        try:
            filter_value = float(form["filter_value"])
        except ValueError:
            filter_value = str(form["filter_value"])
        df_filtered = df[comparison_operator(df[filter_area].values, filter_value)]

    elif properties["query"] == "annotation_code":
        import json
        with open('static/salmonella_annotations.json') as json_file:
            salmonella_annotations = json.load(json_file)
        df_genes = df[filter_area].tolist()
        filter_value = []
        print(properties["code_type"])
        for salmonella_locus in salmonella_annotations:
            try:
                if salmonella_locus in df_genes and form["filter_annotation"] in list(salmonella_annotations[salmonella_locus][properties["code_type"]]):
                    filter_value.append(salmonella_locus)
            except TypeError:
                pass
        df_filtered = df[df[filter_area].isin(filter_value)]
    return df_filtered
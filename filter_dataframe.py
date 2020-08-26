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
        comparison_operator, filter_area, any_column = setup_query_parameters(block["forms"], df)
        df_mask = filter_for(block["forms"], block["properties"], df, comparison_operator, filter_area)
        if block_type == "filter":
            if len(df_mask.shape) > 1: # If the mask_area is larger than one column, we need to convert the mask from a 2D array to a 1D list.
                df_mask = list(df_mask) # Maybe bad. This converts the df_mask to a python list, only in certain circumstances. Replacing values in the 2D array isn't easy otherwise.
                for i in range(len(df_mask)):
                    # You can swap True with False to filter for rows where ALL columns satisfy the filter_value.
                    if any_column in df_mask[i]:
                        df_mask[i] = any_column
                    else:
                        df_mask[i] = not any_column
            df = df[df_mask]
        elif block_type == "transformation":
            print(block["forms"]["target_value"])
            # df.loc[df_mask, filter_area] = block["forms"]["target_value"]
            df[filter_area] = df[filter_area].where(~df_mask, other=block["forms"]["target_value"])
            # df = df.where(~df_mask, other=10)
    return df

def setup_query_parameters(forms, df):
    if forms["filter_area"] == "all columns":
        any_column = False
    else:
        any_column = True # If this is set to False, all columns must satisfy the filter value.
    try:
        comparison_operator = COMPARISON_OPERATORS[forms["logical_operator"]]
    except KeyError:
        # If no comparison operator is explicity given, set it to "equal (=)"
        comparison_operator = operator.eq
    try:
        if forms["filter_area"] == "any column" or forms["filter_area"] == "all columns":
            if comparison_operator == operator.eq:
                filter_area = list(df.columns)
            else:
                filter_area = list(df.select_dtypes(include=[np.number]).columns)
        else:
            filter_area = forms["filter_area"]
    except KeyError:
        filter_area = list(df.select_dtypes(include=[np.number]).columns)
    return comparison_operator, filter_area, any_column

def filter_for(forms, properties, df, comparison_operator, filter_area):
    if properties["query"] == "expression": # Directly search for the entered string
        try: # Filter for integers and floats
            filter_value = float(forms["filter_value"])
            df_mask = comparison_operator(df[filter_area].values, filter_value)
            print('df_mask: ', df_mask)
        except ValueError: # Filter for string or semi-colon-seperated list of strings
            filter_value = str(forms["filter_value"]).split('; ')
            print(filter_value)
            print('made it')
            df_mask = df[filter_area].isin(filter_value).values
            print(df_mask)
    elif properties["query"] == "annotation_code": # Search for locus tag's that include the entered annotation id (GO, KEGG, COG, etc.)
        import json
        with open('static/salmonella_annotations.json') as json_file:
            salmonella_annotations = json.load(json_file)
        df_genes = df[filter_area].tolist()
        filter_value = []
        print(properties["code_type"])
        for salmonella_locus in salmonella_annotations:
            try:
                if salmonella_locus in df_genes and forms["filter_annotation"] in list(salmonella_annotations[salmonella_locus][properties["code_type"]]):
                    filter_value.append(salmonella_locus)
            except TypeError:
                pass
        df_mask = df[filter_area].isin(filter_value)
    return df_mask

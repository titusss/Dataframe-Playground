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
    print('df_index: ', df)
    try:
        selection = query['column']
    except KeyError:
        selection = df.columns
    else:
        selection = df.columns
    print(COMPARISON_OPERATORS[query["logical_operator"]["selected"]])
    print(query["value"]["selected"])
    df_filtered = eval('df[df[selection]'+ COMPARISON_OPERATORS[query["logical_operator"]["selected"]] + query["value"]["selected"]+']') # DANGER DANGER DANGER!!! ADD EXCEPTIONS AND WHITELISTS TO EVAL()!!!!
    df_filtered.fillna(0, inplace=True)
    df.reset_index(inplace=True)
    print('df_filtered: ', df_filtered)
    return df_filtered

def main(query, df):
    for array in query:
        print('array')
        print(array)
        for block in array:
            print('block')
            print(block)
            if block['logical_operator']!='':
                df_filtered = value_filter(block, df)
                print(df_filtered)
    return df_filtered
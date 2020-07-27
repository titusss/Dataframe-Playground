import pandas as pd # NOTE: Maybe unnecessary? No np. references.

def main(transformation_type, metadata, df_old, df_new):
    print('transform_main')
    df_transformed = TRANSFORMATION_FUNCTIONS[transformation_type](metadata, df_old, df_new)
    return df_transformed

def relative_expression(metadata, df_old, df_new):
    print(df_old)
    print(df_new)
    import numpy as np
    print(metadata['transformation']['options']['activated'])
    if metadata['transformation']['options']['activated'] == False: # NOTE: This should check for True, but the vue.js matrix component binds the boolean wrong
        print('ayayaaaa')
        print(df_old)
        print(df_new)
        df_old_log = np.log(df_old.select_dtypes(include=[np.number])) / np.log(metadata['transformation']['options']['value']) # Create log with base of option.value for old df
        df_new_log = np.log(df_new.select_dtypes(include=[np.number])) / np.log(metadata['transformation']['options']['value'])
        print('here')
        df_transformed = df_old_log.select_dtypes(include=[np.number]) / df_new_log.select_dtypes(include=[np.number])
        print('there')
        print(df_transformed)
    else:
        print('no_log')
        df_transformed = df_old / df_new
    df_transformed.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_transformed.fillna(0, inplace=True)
    print(df_transformed)
    return df_transformed

TRANSFORMATION_FUNCTIONS = {
    "relative_expression": relative_expression
}
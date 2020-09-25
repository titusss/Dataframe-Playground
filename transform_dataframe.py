import pandas as pd # NOTE: Maybe unnecessary? No np. references.

def main(transformation_type, metadata, df):
    df_transformed = TRANSFORMATION_FUNCTIONS[transformation_type](metadata, df)
    return df_transformed

# def relative_expression(metadata, df_old, df_new):
#     import numpy as np
#     print(metadata['transformation']['options']['activated'])
#     if metadata['transformation']['options']['activated'] == False: # NOTE: This should check for True, but the vue.js matrix component binds the boolean wrong
#         df_old_log = np.log(df_old.select_dtypes(include=[np.number])) / np.log(float(metadata['transformation']['options']['value'])) # Create log with base of option.value for old df
#         df_new_log = np.log(df_new.select_dtypes(include=[np.number])) / np.log(float(metadata['transformation']['options']['value']))
#         df_transformed = np.round(df_old_log.select_dtypes(include=[np.number]) / df_new_log.select_dtypes(include=[np.number]), 3)
#     else:
#         df_transformed = np.round(df_old.select_dtypes(include=[np.number]) / df_new.select_dtypes(include=[np.number]), 3)
#     print(df_transformed)
#     df_transformed.replace([np.inf, -np.inf], np.nan, inplace=True)
#     # df_transformed = df_transformed.dropna()
#     # df_transformed = df_transformed.replace({np.nan: None})
    
#     df_transformed.fillna(0, inplace=True)
#     print('df_transformed: ', df_transformed)
#     df_old[df_transformed.columns] = df_transformed
#     df_transformed = df_old
#     print(df_transformed)
#     return df_transformed

def count_transcript_length(metadata, df):
    print(metadata)
    df[metadata["new_column_title"]] = df[metadata["end_column_title"]] - df[metadata["start_column_title"]]
    # print(df)
    return df

def count_to_tpm(metadata, df):
    df["eff_leng"] = df[metadata["end_column_title"]] - df[metadata["start_column_title"]]
    rate = np.log(df["filter_area"]) / np.log(df["eff_leng"])
    



TRANSFORMATION_FUNCTIONS = {
    # "relative_expression": relative_expression,
    "count_transcript_length": count_transcript_length
}
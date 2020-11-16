import pandas as pd # NOTE: Maybe unnecessary? No np. references.

<<<<<<< HEAD
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
    df_old[df_transformed.columns] = df_transformed
    print('df_old:', df_old)
    df_transformed = df_old
    print(df_transformed)
    return df_transformed

TRANSFORMATION_FUNCTIONS = {
    "relative_expression": relative_expression
=======
def main(transformation_type, metadata, df, unfiltered_df):
    df_transformed = TRANSFORMATION_FUNCTIONS[transformation_type](metadata, df, unfiltered_df)
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

def count_transcript_length(metadata, df, unfiltered_df):
    df[metadata["new_column_title"]] = df[metadata["end_column_title"]] - df[metadata["start_column_title"]]
    return df

def calculate_tpm(metadata, df, unfiltered_df):
    print(unfiltered_df)
    print(df)
    transcript_length = df[metadata["end_column_title"]] - df[metadata["start_column_title"]]
    import numpy as np
    args = {metadata["counts_column"] : df[metadata["counts_column"]] / transcript_length * (1 / (unfiltered_df[metadata["counts_column"]].sum()) * (df[metadata["counts_column"]] / transcript_length)) * 1e6}
    df = df.assign(**args)
    df.rename(columns={metadata["counts_column"]: "TPM "+metadata["counts_column"]}, inplace=True)
    return df
    


TRANSFORMATION_FUNCTIONS = {
    # "relative_expression": relative_expression,
    "count_transcript_length": count_transcript_length,
    "calculate_tpm": calculate_tpm
>>>>>>> Moved backend to dedicated Container folder.
}
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
    unfiltered_df = df.copy()
    # print(query)
    # import experimental_features
    # df = experimental_features.adjust_numeric_dtype(df) # This reduces the dataframe's size by around 50% but increases computation time by 30% and needs rounding due to lower FP precision
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
        elif block_type == "replace":
            try:
                target_value = float(block["forms"]["target_value"])
            except ValueError:
                target_value = block["forms"]["target_value"]
            print(filter_area)
            print(df_mask)
            df[filter_area] = df[filter_area].where(~df_mask, other=target_value)
            print(df[filter_area])
            if type(filter_area) == list:
                for column in filter_area:
                    df[column] = pd.to_numeric(df[column], downcast="integer", errors="ignore") # If all values of the target column are now numeric, try to change the dtype of that column to numeric
            else:
                df[filter_area] = pd.to_numeric(df[filter_area], downcast="integer", errors="ignore")
        elif block_type == "hide":
            if block["forms"]["target_column"] == "all columns":
                target_area = list(df.columns)
            else:
                target_area = block["forms"]["target_column"]
            df.drop(target_area, axis=1, inplace=True)
        elif block_type == "logarithmic":
            # df[filter_area] = np.round(np.log(df[filter_area].values) / np.log(float(block["forms"]["log_value"])), 3) # NOTE: PERFORMANCE: Be careful with rounding when it comes to precision and performance. Maybe use pandas rounding function.
            df[filter_area] = np.log(df[filter_area].values) / np.log(float(block["forms"]["log_value"]))
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
        elif block_type == "fold_change":
            # df[filter_area] = np.round(df[filter_area].div(df[block["forms"]["target_column"]].values,axis=0), 3) # NOTE: PERFORMANCE: Be careful with rounding when it comes to precision and performance. Maybe use pandas rounding function.
            df[filter_area] = df[filter_area].div(df[block["forms"]["target_column"]].values,axis=0)
            try:
                # For relative gene expression. NOTE: Dividing first and calculating the log AFTER might loose precision.
                # Alternative would be to calculate log(df) - log(target_column).
                # df[filter_area] = np.round(np.log(df[filter_area].values) / np.log(float(block["forms"]["log_value"])), 3) # NOTE: PERFORMANCE: Be careful with rounding when it comes to precision and performance. Maybe use pandas rounding function.
                df[filter_area] = np.log(df[filter_area].values) / np.log(float(block["forms"]["log_value"]))
            except:
                pass
            df.drop(block["forms"]["target_column"], axis=1, inplace=True) # Remove base columns.
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
        elif block_type == "round":
            if block["forms"]["target_column"] == "all columns":
                target_area = list(df.columns)
            else:
                target_area = block["forms"]["target_column"]
            df[filter_area] = np.round(df[filter_area], int(block["forms"]["round_value"]))
        elif block_type == "transcript_length":
            metadata = {
                "start_column_title": filter_area,
                "end_column_title": block["forms"]["target_column"],
                "new_column_title": block["forms"]["target_value"]
            }
            import transform_dataframe
            df = transform_dataframe.main("count_transcript_length", metadata, df, unfiltered_df)
        elif block_type == "calculate_tpm":
            metadata = {
                "start_column_title": block["forms"]["start_column"],
                "end_column_title": block["forms"]["end_column"],
                "counts_column": block["forms"]["counts_column"]
            }
            import transform_dataframe
            df = transform_dataframe.main("calculate_tpm", metadata, df, unfiltered_df)
        elif block_type == "convert_to_index":
            if block["forms"]["target_column"] == "all columns":
                target_area = list(df.columns)
            else:
                target_area = [block["forms"]["target_column"]]
            for target_column in target_area:
                if target_column.startswith("("):
                    try:
                        df[target_column] = df[target_column].astype(str)
                        df.rename(columns={target_column: target_column.split(") ", 1)[1]}, inplace=True)
                    except IndexError as e:
                        pass
    return df

def setup_query_parameters(forms, df):
    # NOTE: This should be reworked. There should be at least 4 functions: 1 for "Filters", 1 for "Hide", 1 for "Transformation", 1 for "Replace"
    any_column = True # If this is set to False, all columns must satisfy the filter value.
    try:
        if forms["filter_area"] == "all columns":
            any_column = False
    except:
        pass
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
                filter_area = list(df.select_dtypes(include=[np.number]).columns) # Only columns with numeric values can be compared when the comparison operator is not equal (=).
        else:
            filter_area = forms["filter_area"]
    except KeyError:
        try:
            string = '(' + forms["target_table"] + ') '
            try:
                filter_area = [col for col in list(df.columns) if col.startswith(string) and col != forms["target_column"]] # If there is a target_table, it'll search for columns that start with '(target_table) '
            except KeyError:
                filter_area = [col for col in list(df.columns) if col.startswith(string)]
            any_column = False
        except KeyError:
            filter_area = list(df.select_dtypes(include=[np.number]).columns)
    return comparison_operator, filter_area, any_column

def filter_for(forms, properties, df, comparison_operator, filter_area):
    if properties["query"] == "expression": # Directly search for the entered string
        try: # Filter for integers and floats
            if forms["filter_value"].lower() != "nan" or forms["filter_value"] == " ":
                filter_value = float(forms["filter_value"])
                df_mask = comparison_operator(df[filter_area].values, filter_value)
            else:
                raise NameError
            # print('df_mask: ', df_mask)
        except ValueError: # Filter for string or semi-colon-seperated list of strings
            filter_value = str(forms["filter_value"]).split('; ')
            df_mask = df[filter_area].isin(filter_value).values
        except NameError:
            # numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
            # print([filter_area])
            # if type(filter_area) != list:
            #     filter_area = [filter_area]
            # filter_area = [x for x in filter_area if x in numeric_columns]
            if forms["logical_operator"] == '= equal to':
                df_mask = pd.isna(df[filter_area].values)
            elif forms["logical_operator"] == '!= not':
                df_mask = pd.notna(df[filter_area].values)
            else:
                raise ValueError("Must use '= equal to' or '!= not' when searching for NaN values.")
    elif properties["query"] == "annotation_code": # Search for locus tag's that include the entered annotation id (GO, KEGG, COG, etc.)
        import json
        with open('static/gene_annotations.json') as json_file:
            gene_annotations = json.load(json_file)
        df_genes = df[filter_area].tolist()
        filter_value = []
        # print(properties["code_type"])
        for gene_locus in gene_annotations:
            if gene_locus in df_genes and forms["filter_annotation"] in list(gene_annotations[gene_locus][properties["code_type"]]):
                filter_value.append(gene_locus)
        df_mask = df[filter_area].isin(filter_value)
    else: # If the filter does not rely on a mask (e.g. dropping a column)
        df_mask = None
    return df_mask

"""
This Module handles Data Loading, Cleaning, and Filtering
for the Business Intelligence Dashboard.
"""

import pandas as pd

def load_clean_data(file):
    """
    Load and clean data from CSV or Excel file.

    Args:
        file: Uploaded file object from Gradio.
    Returns:
        data: Cleaned pandas DataFrame or None if there are any errors
        message: Status message regarding the data loading process.
    """

    data = None
    message = ""
    missing_values = {}

    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file.name)
        elif file.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file.name)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except ValueError as e:
        message = str(e)
        return data, message, missing_values
    except Exception as e:
        message = "No file uploaded. Please upload a valid CSV or Excel file."
        return data, message, missing_values
    
    if data is not None:
        # Find missing values
        missing_values = data.isnull().sum().to_dict()

        numeric_cols = data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            data[col] = data[col].fillna(data[col].mean())

        # Drop rows with any remaining missing values
        data = data.dropna().reset_index(drop=True)
        message = "Data loaded and cleaned successfully."
        return data, message, missing_values
    else:
        message = "Failed to load and clean data."
        return data, message

def get_data_info(data):
    """
    Get basic information about the dataset.

    Args:
        data: pandas DataFrame
    Returns:
        A tuple containing:
            - Number of rows
            - Number of columns
            - List of column names
            - Dictionary of data types for each column
        None if data is None
    """
    if data is not None:
        num_rows = data.shape[0]
        num_cols = data.shape[1]
        col_names = data.columns.tolist()
        data_types = data.dtypes.apply(lambda x: x.name).to_dict()

        return (num_rows, num_cols, col_names, data_types)
    else:
        return None

def preview_data(data, num_rows=5, first=True, last=False):
    """
    Preview first and/or last rows of the dataset.

    Args:
        data: pandas DataFrame
        num_rows: Number of rows to preview from start/end
        first: Boolean indicating whether to return first rows
        last: Boolean indicating whether to return last rows
    Returns:
        A tuple containing:
            - DataFrame of first rows (or None)
            - DataFrame of last rows (or None)  
    """

    first_rows = None
    last_rows = None
    if data is not None:
        if first:
            first_rows = data.head(num_rows)
        if last:
            last_rows = data.tail(num_rows)   
        return first_rows, last_rows
    else:
        return None, None
    
def numeric_filter(data, column, min, max):
    """
    Applies a numeric filter on the specified column

    Args:
        data: pandas DataFrame
        column: Column name to apply the filter on
        min: Minimum value for the filter
        max: Maximum value for the filter
    Returns:
        filtered pandas DataFrame
    """

    if data is None or column not in data.columns or not pd.api.types.is_numeric_dtype(data[column]):
        return data

    if min is not None and max is not None:
        filtered_data = data[(data[column] >= min) & (data[column] <= max)]
        return filtered_data
    elif min is not None:
        filtered_data = data[data[column] >= min]
        return filtered_data
    elif max is not None:
        filtered_data = data[data[column] <= max]
        return filtered_data
    else:
        return data

def categorical_filter(data, column, selected_categories):
    """
    Applies a categorical filter on the specified column

    Args:
        data: pandas DataFrame
        column: Column name to apply the filter on
        selected_categories: List of categories to filter by
    Returns:
        filtered pandas DataFrame
    """

    if data is None or column not in data.columns or not pd.api.types.is_categorical_dtype(data[column]) and not pd.api.types.is_object_dtype(data[column]):
        return data

    if selected_categories and len(selected_categories) > 0:
        filtered_data = data[data[column].isin(selected_categories)]
        return filtered_data
    else:
        return data

def date_filter(data, column, start_date, end_date):
    """
    Applies a date filter on the specified column

    Args:
        data: pandas DataFrame
        column: Column name to apply the filter on
        start_date: Start date for the filter
        end_date: End date for the filter
    Returns:
        filtered pandas DataFrame
    """

    if data is None or column not in data.columns or not pd.api.types.is_datetime64_any_dtype(data[column]):
        return data

    if start_date is not None and end_date is not None:
        filtered_data = data[(data[column] >= start_date) & (data[column] <= end_date)]
        return filtered_data
    elif start_date is not None:
        filtered_data = data[data[column] >= start_date]
        return filtered_data
    elif end_date is not None:
        filtered_data = data[data[column] <= end_date]
        return filtered_data
    else:
        return data

def filter_data(data, filters_config=None, numeric_cols=None, categorical_cols=None, datetime_cols=None):
    """
    Unified filtering function that applies single or multiple filters to a DataFrame.
    
    Args:
        data: pandas DataFrame
        filters_config: Dictionary where keys are column names and values are filter configurations
                       Example: {
                           'age': {'type': 'numeric', 'min': 20, 'max': 50},
                           'city': {'type': 'categorical', 'values': ['NYC', 'LA']},
                           'date': {'type': 'date', 'start': '2024-01-01', 'end': '2024-12-31'}
                       }
                       Can also be a single column dict or empty dict
        numeric_cols: List of numeric column names
        categorical_cols: List of categorical column names
        datetime_cols: List of datetime column names
    Returns:
        Filtered pandas DataFrame
    """
    if data is None:
        return data
    
    if not filters_config:
        return data
    
    filtered_data = data.copy()
    
    # Apply each filter in the configuration
    for column, filter_info in filters_config.items():
        if column not in data.columns:
            continue
        
        filter_type = filter_info.get('type')
        
        # Apply numeric filter
        if filter_type == 'numeric' and numeric_cols and column in numeric_cols:
            min_val = filter_info.get('min')
            max_val = filter_info.get('max')
            if min_val is not None and max_val is not None:
                filtered_data = numeric_filter(filtered_data, column, min_val, max_val)
        
        # Apply categorical filter
        elif filter_type == 'categorical' and categorical_cols and column in categorical_cols:
            selected_values = filter_info.get('values', [])
            if selected_values:
                filtered_data = categorical_filter(filtered_data, column, selected_values)
        
        # Apply date filter
        elif filter_type == 'date' and datetime_cols and column in datetime_cols:
            start_date = filter_info.get('start')
            end_date = filter_info.get('end')
            filtered_data = date_filter(filtered_data, column, start_date, end_date)
    
    return filtered_data

def get_filtered_data_row_count(data):
    """
    Get the number of rows in the filtered dataset.

    Args:
        data: pandas DataFrame
    Returns:
        Number of rows in the DataFrame or 0 if data is None
    """
    if data is not None:
        return data.shape[0]
    else:
        return 0





    



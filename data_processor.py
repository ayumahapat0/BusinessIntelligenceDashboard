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
    



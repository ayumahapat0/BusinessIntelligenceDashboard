"""
This class handles all Utility functions for Statistics

Numeric: Mean, Median, Std, min, max, quartiles
Categoric: Mode, unique values, mode
Missing Values: Count
"""

import pandas as pd


def compute_numeric_stats(data, column):
    """
    Compute basic statistics for a numeric column.

    Args:
        data: pandas DataFrame
        column: Column name for which to compute statistics.
    Returns:
        A dictionary containing mean, median, std, min, max, and quartiles.
    """

    if data is None or column not in data.columns:
        return {}

    stats = {}
    if column in data.select_dtypes(include=['number']).columns:
        stats['mean'] = float(data[column].mean())
        stats['median'] = float(data[column].median())
        stats['std'] = float(data[column].std())
        stats['min'] = float(data[column].min())
        stats['max'] = float(data[column].max())
        stats['25%'] = float(data[column].quantile(0.25))
        stats['50%'] = float(data[column].quantile(0.50))
        stats['75%'] = float(data[column].quantile(0.75))
    return stats

def compute_categoric_stats(data, column):
    """
    Compute basic statistics for a categorical column.

    Args:
        data: pandas DataFrame
        column: Column name for which to compute statistics.
    Returns:
        A dictionary containing unique values, mode, and value counts.
    """
    if data is None or column not in data.columns:
        return {}

    stats = {}
    if column in data.select_dtypes(include=['object', 'category']).columns:
        stats['unique_values'] = data[column].unique().tolist()
        stats['mode'] = data[column].mode()[0] if not data[column].mode().empty else None
        stats['value_counts'] = data[column].value_counts().to_dict()
    return stats

def missing_values_count(file):
    """
    Compute the count of missing values for each column.

    Args:
        file: Uploaded file object from Gradio.
    Returns:
        A dictionary with column names as keys and missing value counts as values.
    """
    data = None
    missing_values = {}

    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file.name)
        elif file.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file.name)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except Exception:
        return missing_values

    if data is not None:
        missing_values = data.isnull().sum().to_dict()
    return missing_values

def correlation_matrix(data):
    """
    Compute the correlation matrix for numeric columns in the dataset.

    Args:
        data: pandas DataFrame
    Returns:
        A pandas DataFrame representing the correlation matrix.
    """
    if data is None:
        return pd.DataFrame()

    numeric_data = data.select_dtypes(include=['number'])
    corr_matrix = numeric_data.corr()
    return corr_matrix

def get_data_cols(data):
    """
    Get the list of column names in the dataset.

    Args:
        data: pandas DataFrame
    Returns:
        
    """
    numeric_cols = []
    categorical_cols = []
    datetime_cols = []

    if data is not None:
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = data.select_dtypes(include=['datetime']).columns.tolist()
        return numeric_cols, categorical_cols, datetime_cols
    
    else:
        return None, None, None

def get_date_range(data, column):
    """
    Get the minimum and maximum dates from a datetime column.

    Args:
        data: pandas DataFrame
        column: Column name for which to get the date range.
    Returns:
        A tuple containing the minimum and maximum dates.
    """
    if data is not None and column in data.columns:
        if column in data.select_dtypes(include=['datetime']).columns:
            min_date = data[column].min()
            max_date = data[column].max()
            return min_date, max_date
        else:
            return None, None
    else:
        return None, None
        





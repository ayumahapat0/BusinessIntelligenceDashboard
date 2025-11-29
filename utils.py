"""
This class handles all Utility functions for Statistics

Numeric: Mean, Median, Std, min, max, quartiles
Categoric: Mode, unique values, mode
Missing Values: Count
"""



import pandas as pd


def compute_numeric_stats(data: pd.DataFrame, column: str) -> dict:
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

def compute_categoric_stats(data: pd.DataFrame, column: str) -> dict:
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

def missing_values_count(file: any) -> dict:
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

def correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
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





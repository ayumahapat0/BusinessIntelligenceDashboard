"""
This Module handles Data Loading, Cleaning, and Filtering
for the Business Intelligence Dashboard.
"""

import pandas as pd

    
# Load and clean data from CSV or Excel file passed from Gradio file upload
def load_clean_data(file):

    try:
        if file.name.endswith('.csv'):
            data = pd.read_csv(file.name)
        elif file.name.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(file.name)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    except Exception as e:
        print(f"Error loading data: {e}")
        data = None
    
    if data is not None:  
        # Fill missing values with column mean for numeric columns
        numeric_cols = data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            data[col] = data[col].fillna(data[col].mean())

        # Drop rows with any remaining missing values
        data = data.dropna().reset_index(drop=True)
        return data
    else:
        print("Need to upload valid data file!")

# Diplay basic info about dataset
def get_data_info(data):
    if data is not None:
        num_rows = data.shape[0]
        num_cols = data.shape[1]
        col_names = data.columns.tolist()
        data_types = data.dtypes.apply(lambda x: x.name).to_dict()

        return (num_rows, num_cols, col_names, data_types)
    else:
        return None

# Show Data Preview
def preview_data(data, num_rows=5, first=True, last=False):
    first_rows = None
    last_rows = None
    if data is not None:
        if first:
            first_rows = data.head(num_rows)
        if last:
            last_rows = data.tail(num_rows)   
        return first_rows, last_rows
    else:
        return None
    



"""
This Modules handles creating visualizations 
for the Business Intelligence Dashboard.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def time_series_plot(data: pd.DataFrame, date_column: str, value_column: str, aggregation: str = 'sum'):
    """
    Create a time series plot for the given date and value columns.

    Args:
        data: pandas DataFrame
        date_column: Column name representing dates.
        value_column: Column name representing values to plot.
    Returns:
        A matplotlib figure object.
    """
    if data is None or date_column not in data.columns or value_column not in data.columns:
        return None
    
    agg = {value_column: aggregation}
    time_series_data = data.groupby(date_column).agg(agg).reset_index()


    plt.figure(figsize=(10, 6))
    sns.lineplot(data=time_series_data, x=date_column, y=value_column)
    plt.title(f'Time Series Plot of {value_column} over {date_column}')
    plt.xlabel(date_column)
    plt.ylabel(value_column)
    plt.tight_layout()
    
    fig = plt.gcf()
    return fig


def distribution_plot(data: pd.DataFrame, column: str, plot_type: str = 'histogram'):

    """
    Create a distribution plot for the given column.

    Args:
        data: pandas DataFrame
        column: Column name to plot the distribution for.
        plot_type: Type of distribution plot ('histogram' or 'boxplot').
    Returns:
        A matplotlib figure object.
    """

    if data is None or column not in data.columns:
        return None
    
    plt.figure(figsize=(8, 6))
    
    if plot_type == 'Histogram':
        sns.histplot(data[column], kde=True)
        plt.title(f'Histogram of {column}')
    elif plot_type == 'Box Plot':
        sns.boxplot(y=data[column])
        plt.title(f'Boxplot of {column}')
    else:
        return None
    
    plt.tight_layout()
    fig = plt.gcf()
    return fig

def category_analysis_plot(data: pd.DataFrame, category_column: str, value_column: str, option: str):

    """
    Create a category analysis plot for the given category and value columns.

    Args:
        data: pandas DataFrame
        category_column: Column name representing categories.
        value_column: Column name representing values to analyze.
        option: Type of plot ('bar chart' or 'pie chart').
    Returns:
        A matplotlib figure object.
    """
    
    if data is None or category_column not in data.columns or value_column not in data.columns:
        return None
    
    category_data = data.groupby(category_column)[value_column].sum().reset_index()
    
    plt.figure(figsize=(8, 6))
    
    if option == 'Bar Chart':
        sns.barplot(data=category_data, x=category_column, y=value_column)
        plt.title(f'Bar Chart of {value_column} by {category_column}')
        plt.xlabel(category_column)
        plt.ylabel(value_column)
    elif option == 'Pie Chart':
        plt.pie(category_data[value_column], labels=category_data[category_column], autopct='%1.1f%%')
        plt.title(f'Pie Chart of {value_column} by {category_column}')
    else:
        return None
    
    plt.tight_layout()
    fig = plt.gcf()
    return fig

def relationship_plot(data: pd.DataFrame, option: str,  x_column: str, y_column: str):

    """
    Create a scatter plot for the given x and y columns.

    Args:
        data: pandas DataFrame
        option: scatter plot or correlation heatmap
        x_column: Column name for x-axis.
        y_column: Column name for y-axis.
    Returns:
        A matplotlib figure object.
    """
    
    if data is None:
        return None
    
    plt.figure(figsize=(8, 6))
    
    if option == 'Scatter Plot':
        if x_column not in data.columns or y_column not in data.columns:
            return None
        sns.scatterplot(data=data, x=x_column, y=y_column)
        plt.title(f'Scatter Plot of {y_column} vs {x_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
    elif option == 'Correlation Heatmap':
        corr = data.corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Heatmap')
    else:
        return None
    
    plt.tight_layout()
    fig = plt.gcf()
    return fig

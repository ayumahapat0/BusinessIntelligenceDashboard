"""
This Modules handles creating visualizations 
for the Business Intelligence Dashboard.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import utils
import tempfile


def time_series_plot(data, date_col, value_col, agg_method):
    """
    Generate time series plot showing trends over time.
    
    Args:
        data: pandas DataFrame
        date_col: Column name for dates (x-axis)
        value_col: Column name for values (y-axis)
        agg_method: Aggregation method ('sum', 'mean', 'count', 'median', 'min', 'max')
    Returns:
        matplotlib figure object or None if validation fails
    """
    if data is None or not date_col or not value_col:
        return None, None
    
    # Validate column types
    numeric_cols, _, datetime_cols = utils.get_data_cols(data)
    
    if date_col not in datetime_cols:
        print(f"Error: {date_col} is not a datetime column")
        return None, None
    
    if value_col not in numeric_cols:
        print(f"Error: {value_col} is not a numeric column")
        return None, None
    
    # Group by date and aggregate
    grouped = data.groupby(date_col)[value_col].agg(agg_method).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(grouped[date_col], grouped[value_col], marker='o', linestyle='-', linewidth=2)
    ax.set_xlabel(date_col, fontsize=12)
    ax.set_ylabel(f"{agg_method.capitalize()} of {value_col}", fontsize=12)
    ax.set_title(f"Time Series: {agg_method.capitalize()} of {value_col} over {date_col}", 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    temp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig.savefig(temp.name)
    
    return fig, temp.name


def distribution_plot(data, column, plot_type):
    """
    Generate distribution plot (histogram or box plot) for numerical data.
    
    Args:
        data: pandas DataFrame
        column: Column name to analyze
        plot_type: 'Histogram' or 'Box Plot'
    Returns:
        matplotlib figure object or None if validation fails
    """
    if data is None or not column:
        return None
    
    # Validate column is numeric
    numeric_cols, _, _ = utils.get_data_cols(data)
    
    if column not in numeric_cols:
        print(f"Error: {column} is not a numeric column")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == "Histogram":
        ax.hist(data[column], bins=30, edgecolor='black', alpha=0.7, color='steelblue')
        ax.set_xlabel(column, fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title(f"Distribution of {column}", fontsize=14, fontweight='bold')
    else:  # Box Plot
        ax.boxplot(data[column], vert=True, patch_artist=True,
                   boxprops=dict(facecolor='lightblue'))
        ax.set_ylabel(column, fontsize=12)
        ax.set_title(f"Box Plot of {column}", fontsize=14, fontweight='bold')
    
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig

def category_analysis_plot(data, cat_col, value_col, agg_method, chart_type):
    """
    Generate category analysis plot (bar chart or pie chart).
    
    Args:
        data: pandas DataFrame
        cat_col: Categorical column name
        value_col: Value column name (optional, for aggregation)
        agg_method: Aggregation method ('count', 'sum', 'mean', 'median')
        chart_type: 'Bar Chart' or 'Pie Chart'
    Returns:
        matplotlib figure object or None if validation fails
    """
    if data is None or not cat_col:
        return None
    
    # Validate column types
    numeric_cols, categorical_cols, _ = utils.get_data_cols(data)
    
    if cat_col not in categorical_cols:
        print(f"Error: {cat_col} is not a categorical column")
        return None
    
    # Check if too many unique values
    num_unique = data[cat_col].nunique()

    # If value column is specified, validate it's numeric
    if value_col and value_col not in numeric_cols:
        print(f"Error: {value_col} is not a numeric column")
        return None
    
    # If no value column or count method, just count occurrences
    if not value_col or agg_method == "count":
        grouped = data[cat_col].value_counts().head(20)
        ylabel = "Count"
    else:
        grouped = data.groupby(cat_col)[value_col].agg(agg_method).sort_values(ascending=False).head(20)
        ylabel = f"{agg_method.capitalize()} of {value_col}"
    
    # Check if we have data to plot after grouping
    if len(grouped) == 0:
        print(f"Error: No data to plot for {cat_col}")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == "Bar Chart":
        ax.bar(range(len(grouped)), grouped.values, edgecolor='black', alpha=0.7, color='coral')
        ax.set_xticks(range(len(grouped)))
        ax.set_xticklabels(grouped.index, rotation=45, ha='right')
        ax.set_xlabel(cat_col, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        
        # Add note if showing limited data
        title = f"{cat_col} Analysis"
        if num_unique > 20:
            title += f" (Top 20 of {num_unique} categories)"
        else:
            title += f" (All {num_unique} categories)"
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
    else:  # Pie Chart
        # Limit to top 10 for pie chart readability
        top_10 = grouped.head(10)
        ax.pie(top_10.values, labels=top_10.index, autopct='%1.1f%%', startangle=90)
        
        title = f"{cat_col} Distribution"
        if num_unique > 10:
            title += f" (Top 10 of {num_unique} categories)"
        else:
            title += f" (All {num_unique} categories)"
        
        ax.set_title(title, fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig

def relationship_plot(data, plot_type, x_col, y_col):
    """
    Generate scatter plot or correlation heatmap.
    
    Args:
        data: pandas DataFrame
        plot_type: 'Scatter Plot' or 'Correlation Heatmap'
        x_col: X-axis column name (for scatter plot)
        y_col: Y-axis column name (for scatter plot)
    Returns:
        matplotlib figure object or None if validation fails
    """
    if data is None:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == "Scatter Plot":
        if not x_col or not y_col:
            return None
        
        # Validate both columns are numeric for scatter plot
        numeric_cols, _, _ = utils.get_data_cols(data)
        
        if x_col not in numeric_cols:
            print(f"Error: {x_col} is not a numeric column")
            return None
        
        if y_col not in numeric_cols:
            print(f"Error: {y_col} is not a numeric column")
            return None
        
        ax.scatter(data[x_col], data[y_col], alpha=0.6, color='mediumseagreen')
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.set_title(f"Scatter Plot: {x_col} vs {y_col}", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
    else:  # Correlation Heatmap
        numeric_data = data.select_dtypes(include=['number'])
        if numeric_data.empty:
            print("Error: No numeric columns available for correlation heatmap")
            return None
        
        corr_matrix = numeric_data.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, cbar_kws={'label': 'Correlation'},
                   square=True, linewidths=0.5)
        ax.set_title("Correlation Heatmap", fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    return fig



"""
This Module handles creating Auomated Insights 
for the Business Intelligence Dashboard.
"""

import pandas as pd
import utils


def generate_top_bottom_performers(data):
    """
    Generate insights about top and bottom performers in the dataset.
    
    Args:
        data: pandas DataFrame
    Returns:
        String containing formatted insights about top/bottom values
    """
    if data is None:
        return "No data loaded."
    
    numeric_cols, _, _ = utils.get_data_cols(data)
    
    if not numeric_cols:
        return "No numeric columns found in the dataset."
    
    performers_insight = "## Top/Bottom Performers\n\n"
    
    # Analyze first 3 numeric columns
    for col in numeric_cols[:3]:
        top_5 = data.nlargest(5, col)[[col]]
        bottom_5 = data.nsmallest(5, col)[[col]]
        
        performers_insight += f"### {col}\n"
        performers_insight += f"**Top 5 Values:**\n"
        for idx, val in top_5[col].items():
            performers_insight += f"- Row {idx}: {val:.2f}\n"
        
        performers_insight += f"\n**Bottom 5 Values:**\n"
        for idx, val in bottom_5[col].items():
            performers_insight += f"- Row {idx}: {val:.2f}\n"
        performers_insight += "\n"
    
    return performers_insight


def generate_trends_and_anomalies(data):
    """
    Generate insights about trends and anomalies in the dataset.
    
    Args:
        data: pandas DataFrame
    Returns:
        String containing formatted insights about trends and anomalies
    """
    if data is None:
        return "No data loaded."
    
    numeric_cols, categorical_cols, _ = utils.get_data_cols(data)
    
    trends_insight = "## Basic Trends and Anomalies\n\n"
    
    # Numeric column analysis
    if numeric_cols:
        trends_insight += "### Numeric Column Analysis\n\n"
        for col in numeric_cols[:3]:  # Analyze first 3 numeric columns
            mean_val = data[col].mean()
            std_val = data[col].std()
            
            # Find anomalies (values beyond 2 standard deviations)
            anomalies = data[(data[col] < mean_val - 2*std_val) | (data[col] > mean_val + 2*std_val)]
            
            trends_insight += f"**{col}:**\n"
            trends_insight += f"- Mean: {mean_val:.2f}\n"
            trends_insight += f"- Std Dev: {std_val:.2f}\n"
            trends_insight += f"- Anomalies detected: {len(anomalies)} values beyond 2σ\n"
            
            if len(anomalies) > 0:
                trends_insight += f"- Anomaly range: {anomalies[col].min():.2f} to {anomalies[col].max():.2f}\n"
            trends_insight += "\n"
    
    # Categorical column analysis
    if categorical_cols:
        trends_insight += "### Categorical Insights\n\n"
        for col in categorical_cols[:2]:  # First 2 categorical columns
            most_common = data[col].mode()[0] if not data[col].mode().empty else "N/A"
            unique_count = data[col].nunique()
            value_counts = data[col].value_counts().head(3)
            
            trends_insight += f"**{col}:**\n"
            trends_insight += f"- Most common value: {most_common}\n"
            trends_insight += f"- Unique values: {unique_count}\n"
            trends_insight += f"- Top 3 frequencies:\n"
            for val, count in value_counts.items():
                trends_insight += f"  - {val}: {count} occurrences\n"
            trends_insight += "\n"
    
    return trends_insight


def generate_all_insights(data):
    """
    Generate all automated insights from the data.
    
    Args:
        data: pandas DataFrame
    Returns:
        Tuple of (performers_insight, trends_insight)
    """
    performers = generate_top_bottom_performers(data)
    trends = generate_trends_and_anomalies(data)
    
    return performers, trends
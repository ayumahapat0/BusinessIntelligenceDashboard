# Business Intelligence Dashboard

A comprehensive data analysis and visualization tool built with Gradio that enables users to upload, explore, filter, and visualize their business data through an intuitive web interface.

## Features

### 📊 Data Management
- **Upload CSV or Excel files** for analysis
- **Data preview** with configurable row display (first/last rows)
- **Dataset information** including row count, column names, and data types
- **Export filtered data** to CSV format

### 📈 Statistics & Analysis
- **Automated summary statistics** for numeric and categorical columns
- **Missing values report** from original dataset
- **Correlation matrix** visualization for numeric columns

### 🔍 Filtering & Exploration
- **Dynamic filtering** by column type:
  - Numeric range filters (min/max)
  - Categorical multi-select filters
  - Date range filters (YYYY-MM-DD format)
- **Real-time filtered row count** tracking
- **Preview filtered results** (first 100 rows)

### 📉 Visualizations
- **Time Series Plots**: Visualize trends over time with multiple aggregation methods
- **Distribution Analysis**: Histograms and box plots for numeric data
- **Category Analysis**: Bar charts and pie charts for categorical data
- **Relationship Analysis**: Scatter plots and correlation heatmaps

### 💡 Automated Insights
- **Top/Bottom Performers**: Identify key data points
- **Trends and Anomalies**: Discover patterns in your dataset

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download the project repository
```bash
git clone https://github.com/ayumahapat0/BusinessIntelligenceDashboard.git
cd BusinessIntelligenceDashboard
```

2. Use a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## How to Run

1. Navigate to the project directory:
```bash
cd BusinessIntelligenceDashboard
```

2. Run the application:
```bash
gradio app.py
```

3. The application will launch in your default web browser. If it doesn't open automatically, look for the local URL in the terminal output (typically `http://127.0.0.1:7860`)

4. Upload your CSV or Excel file and start exploring your data!

## Usage Tips

- **Data Upload**: Start by uploading your data file in the "Data Upload" tab
- **Statistics**: View comprehensive statistics before filtering or visualizing
- **Filtering**: Apply one filter at a time; use "Clear Current Filter" to reset before applying a new filter
- **Visualizations**: Select appropriate columns based on your data types for meaningful charts
- **Insights**: Generate automated insights after uploading your data

## Supported File Formats

- CSV (.csv)
- Excel (.xlsx, .xls)

## Notes

- The application automatically handles missing values during data loading
- Filtered data previews are limited to the first 100 rows for performance
- Categorical columns with more than 100 unique values are limited in the filter dropdown
- All visualizations are interactive and can be downloaded

## Troubleshooting

If you encounter issues:
- Ensure all required Python packages are installed
- Check that your data file is properly formatted
- Verify that date columns are in YYYY-MM-DD format for date filtering
- Make sure all module files (data_processor.py, utils.py, etc.) are in the same directory as app.py
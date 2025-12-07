import gradio as gr
import pandas as pd
import data_processor
import utils
import visualization
import insights

"""
This is the gradio interface
for the Business Intelligence Dashboard.
"""

def create_dashboard():
    with gr.Blocks() as demo:
        gr.Markdown("# Business Intelligence Dashboard")
        
        df_state = gr.State(None)  # To hold the DataFrame across tabs

        file_input = gr.State(None)  # To hold uploaded file info

        missing_values = gr.State(None)  # To hold missing values info

        current_filter = gr.State(None)  # To hold active filters across sessions

        def load_data(file_input):
            """
            Load and clean data using data_processor module.
            
            Args:
                file_input: Uploaded file object from Gradio.
            Returns:
                data: Cleaned pandas DataFrame or None if there are any errors
                string: Status message regarding the data loading process.
            """
            
            data, string, missing_values = data_processor.load_clean_data(file_input)
            
            if data is None:
                return data, string, missing_values
            
            return data, "Data loaded successfully.", missing_values
        
        def display_data_info(data):
            """
            Display basic information about the dataset using data_processor module.

            Args:
                data: pandas DataFrame
            Returns:
                A tuple containing:
                    - Number of rows or ("No data loaded.")
                    - Number of columns or ("No data loaded.")
                    - List of column names or ("No data loaded.")
                    - Dictionary of data types for each column or ("No data loaded.")
            """
            info = data_processor.get_data_info(data)
            if info:
                rows = info[0]
                cols = info[1]
                col_names = f' \n'.join(info[2])
                data_types = f' \n'.join([f"{k}: {v}" for k, v in info[3].items()]) 
                return f"{rows}", f"{cols}", f"{col_names}",f"{data_types}"
            else:
                return "No data loaded.", "No data loaded.", "No data loaded.", "No data loaded."
        
        def preview_data_fn(data, num_rows, first, last):
            """
            Preview first and/or last rows of the dataset using data_processor module.

            Args:
                data: pandas DataFrame
                num_rows: Number of rows to preview
                first: Boolean indicating whether to show first rows
                last: Boolean indicating whether to show last rows
            Returns:
                A tuple containing:
                    - DataFrame of first rows (or None)
                    - DataFrame of last rows (or None)
            """
            first, last = data_processor.preview_data(data, num_rows=num_rows, first=first, last=last)
            if first is None and last is None:
                return None, None
            return first, last
        
        def compute_statistics(data, missing_values):
            """
            Compute and return summary statistics for the dataset.
            Args:
                data: pandas DataFrame
            Returns:
                3 strings containing summary statistics for numeric and categorical columns.
            """
            if data is None:
                return "No data loaded.", "No data loaded.", "No data loaded.", None

            numeric_stats = {}
            categoric_stats = {}

            for col in data.columns:
                if col in data.select_dtypes(include=['number']).columns:
                    stats = utils.compute_numeric_stats(data, col)
                    numeric_stats[col] = stats
                elif col in data.select_dtypes(include=['object', 'category']).columns:
                    stats = utils.compute_categoric_stats(data, col)
                    categoric_stats[col] = stats
            
            numeric = ""
            for col, stats in numeric_stats.items():
                numeric += f"**{col}**:\n"
                for stat_name, value in stats.items():
                    numeric += f"- {stat_name}: {value}\n"
                numeric += "\n"
            
            categorical = ""
            for col, stats in categoric_stats.items():
                categorical += f"**{col}**:\n"
                for stat_name, value in stats.items():
                    categorical += f"- {stat_name}:\n"
                    if stat_name == 'unique_values':
                        for val in value:
                            categorical += f"  - {val}\n"
                    elif stat_name == 'value_counts':
                        for val, count in value.items():
                            categorical += f"  - {val}: {count}\n"
                    else:
                        categorical += f"  - {value}\n"
                categorical += "\n"
            
            missing = ""
            for col, count in missing_values.items():
                missing += f"- {col}: {count}\n" 

            correlation_matrix = utils.correlation_matrix(data)
            
            return numeric, categorical, missing, correlation_matrix

        def update_filter_options(data):
            """Update dropdown with available columns when data is loaded."""
            if data is None:
                return gr.update(choices=[]), "0", "0", None, gr.update(choices=[])
            
            total_rows = len(data)
            return (
                gr.update(choices=data.columns.tolist()),
                str(total_rows),
                str(total_rows),
                data.head(100),
                gr.update(choices=[])
            )
        
        def update_inputs_for_column(data, column):
            """Update the input fields based on the selected column type."""
            if data is None or not column:
                return gr.update(), gr.update(), gr.update(choices=[]), gr.update(), gr.update()
            
            numeric_cols, categorical_cols, datetime_cols = utils.get_data_cols(data)
            
            # Update numeric inputs if numeric column
            if column in numeric_cols:
                min_val = float(data[column].min())
                max_val = float(data[column].max())
                return (
                    gr.update(value=min_val),
                    gr.update(value=max_val),
                    gr.update(choices=[]),
                    gr.update(),
                    gr.update()
                )
            
            # Update categorical dropdown if categorical column
            elif column in categorical_cols:
                unique_vals = data[column].unique().tolist()
                # Turn each into strings
                unique_vals = [str(val) for val in unique_vals]
                num_unqiue = len(unique_vals)

                if num_unqiue > 100:
                    unique_vals = sorted(unique_vals)[:100]  # Limit to first 100 unique values
                    return (
                        gr.update(),
                        gr.update(),
                        gr.update(choices=unique_vals, value=[]),
                        gr.update(),
                        gr.update()
                    )
                else:
                    return (
                        gr.update(),
                        gr.update(),
                        gr.update(choices=unique_vals, value=unique_vals),
                        gr.update(),
                        gr.update()
                    )
            
            # Update date inputs if datetime column
            elif column in datetime_cols:
                min_date, max_date = utils.get_date_range(data, column)
                
                if min_date and max_date:
                    min_date_str = min_date.strftime('%Y-%m-%d')
                    max_date_str = max_date.strftime('%Y-%m-%d')
                else:
                    min_date_str = ""
                    max_date_str = ""
                
                return (
                    gr.update(),
                    gr.update(),
                    gr.update(choices=[]),
                    gr.update(value=min_date_str),
                    gr.update(value=max_date_str)
                )
            
            else:
                return gr.update(), gr.update(), gr.update(choices=[]), gr.update(), gr.update()
        
        def add_numeric_filter_to_state(data, column, num_min, num_max):
            """Apply a numeric filter to a single column."""
            if data is None or not column:
                return None, None, "0"
            
            # Validate column is numeric
            numeric_cols, _, _ = utils.get_data_cols(data)
            if column not in numeric_cols:
                return None, None, "0"
            
            min_val = num_min if num_min is not None else data[column].min()
            max_val = num_max if num_max is not None else data[column].max()
            
            filter_config = {
                column: {
                    'type': 'numeric',
                    'min': min_val,
                    'max': max_val
                }
            }
            
            # Apply filter
            numeric_cols, categorical_cols, datetime_cols = utils.get_data_cols(data)
            filtered_data = data_processor.filter_data(
                data, filter_config, numeric_cols, categorical_cols, datetime_cols
            )
            
            row_count = data_processor.get_filtered_data_row_count(filtered_data)
            return filter_config, filtered_data.head(100), str(row_count)
        
        def add_categorical_filter_to_state(data, column, selected_values):
            """Apply a categorical filter to a single column."""
            if data is None or not column or not selected_values:
                return None, None, "0"
            
            # Validate column is categorical
            _, categorical_cols, _ = utils.get_data_cols(data)
            if column not in categorical_cols:
                return None, None, "0"
            
            filter_config = {
                column: {
                    'type': 'categorical',
                    'values': selected_values
                }
            }
            
            # Apply filter
            numeric_cols, categorical_cols, datetime_cols = utils.get_data_cols(data)
            filtered_data = data_processor.filter_data(
                data, filter_config, numeric_cols, categorical_cols, datetime_cols
            )
            
            row_count = data_processor.get_filtered_data_row_count(filtered_data)
            return filter_config, filtered_data.head(100), str(row_count)
        
        def add_date_filter_to_state(data, column, start_date, end_date):
            """Apply a date filter to a single column."""
            if data is None or not column:
                return None, None, "0"
            
            # Validate column is datetime
            _, _, datetime_cols = utils.get_data_cols(data)
            if column not in datetime_cols:
                return None, None, "0"
            
            filter_config = {
                column: {
                    'type': 'date',
                    'start': start_date,
                    'end': end_date
                }
            }
            
            # Apply filter
            numeric_cols, categorical_cols, datetime_cols = utils.get_data_cols(data)
            filtered_data = data_processor.filter_data(
                data, filter_config, numeric_cols, categorical_cols, datetime_cols
            )
            
            row_count = data_processor.get_filtered_data_row_count(filtered_data)
            return filter_config, filtered_data.head(100), str(row_count)
        
        def clear_current_filter(data):
            """Clear the current filter and show original data."""
            if data is None:
                return None, None, "0"
            
            total_rows = str(len(data))
            return None, data.head(100), total_rows
        

        def update_visualization_options(data):
            """Update visualization dropdowns when data is loaded."""
            if data is None:
                empty = gr.update(choices=[])
                return empty, empty, empty, empty, empty, empty, empty
            
            numeric_cols, categorical_cols, datetime_cols = utils.get_data_cols(data)
            all_cols = data.columns.tolist()
            
            return (
                gr.update(choices=datetime_cols if datetime_cols else []),  # ts_date_col
                gr.update(choices=numeric_cols if numeric_cols else []),    # ts_value_col
                gr.update(choices=numeric_cols if numeric_cols else []),    # dist_col
                gr.update(choices=categorical_cols if categorical_cols else []),  # cat_col
                gr.update(choices=numeric_cols if numeric_cols else []),    # cat_value_col
                gr.update(choices=all_cols),  # scatter_x_col
                gr.update(choices=all_cols)   # scatter_y_col
            )
        
        with gr.Tab("Data Upload"):
            with gr.Row():
                with gr.Column():
                    
                    # File upload
                    gr.Markdown("## Upload Your CSV or Excel Data File")
                    
                    file_input = gr.File(label="Upload CSV or Excel File")
                    
                    upload_btn = gr.Button("Upload Data File")
                
                    upload_btn.click(
                        fn = load_data,
                        inputs = [file_input],
                        outputs = [df_state, gr.Textbox(label="Upload Status", lines=2), missing_values],
                    )
                with gr.Column():
                    
                    # Display Data info
                    gr.Markdown("## Display Dataset Information")
                    
                    data_preview_btn = gr.Button("Display Data Info")
                    
                    rows = gr.Textbox(label="Number of Rows")
                    cols = gr.Textbox(label="Number of Columns")
                    col_names = gr.Textbox(label="Column Names", lines=10)
                    data_types = gr.Textbox(label="Data Types", lines=10)
                    
                    data_preview_btn.click(
                        fn = display_data_info,
                        inputs = [df_state],
                        outputs = [rows, cols, col_names, data_types]
                    )
                
            with gr.Row():
                with gr.Column():
                    
                    # Data Preview
                    gr.Markdown("## Display First/Last Rows of Dataset")
                    
                    data_preview_btn = gr.Button("Preview Data")

                    first_checkbox = gr.Checkbox(label="Show First Rows", value=False)
                    last_checkbox = gr.Checkbox(label="Show Last Rows", value=False)
                    num_rows_input = gr.Slider(1, 50, value=5, step=1, label="Number of Rows to Preview")
                    
                    first_rows_preview = gr.Dataframe(label="First Rows Preview")
                    last_rows_preview = gr.Dataframe(label="Last Rows Preview")
                    
                    data_preview_btn.click(
                        fn = preview_data_fn,
                        inputs = [df_state, num_rows_input, first_checkbox, last_checkbox],
                        outputs = [first_rows_preview, last_rows_preview],
                    )
            
        
        with gr.Tab("Statistics"):
            #Automated statistics
            gr.Markdown("## Summary Statistics of the Dataset")
            stats_btn = gr.Button("Compute Statistics")
            numeric_textbox = gr.Textbox(label="Numeric Statistics", lines=10)
            categoric_textbox = gr.Textbox(label="Categorical Statistics", lines=10)
            missing_values_output = gr.Textbox(label="Missing Values Statistics Before Dataset for cleaned", lines=10)
            correlation_matrix_output = gr.Matrix(label="Correlation Matrix Heatmap")

            stats_btn.click(
                fn = compute_statistics,
                inputs = [df_state, missing_values],
                outputs = [numeric_textbox, categoric_textbox, missing_values_output, correlation_matrix_output]
            )
            
        
        with gr.Tab("Filter & Explore"):
            gr.Markdown("## Filter and Explore Data")
            gr.Markdown("### Filter one column at a time. Select a column and use the appropriate filter type.")
            
            with gr.Row():
                # Left Panel: Filter Controls
                with gr.Column(scale=1):
                    gr.Markdown("### Select Column to Filter")
                    filter_column_select = gr.Dropdown(
                        label="Column",
                        choices=[],
                        interactive=True
                    )
                    
                    # Numeric Filter Section
                    gr.Markdown("**Numeric Filter (Range)**")
                    with gr.Row():
                        numeric_min_input = gr.Number(label="Min Value", interactive=True)
                        numeric_max_input = gr.Number(label="Max Value", interactive=True)
                    apply_numeric_filter_btn = gr.Button("Apply Numeric Filter", variant="primary", size="sm")
                    
                    # Categorical Filter Section
                    gr.Markdown("**Categorical Filter (Multi-Select)**")
                    category_dropdown = gr.Dropdown(
                        label="Select Values",
                        choices=[],
                        multiselect=True,
                        interactive=True
                    )
                    apply_categorical_filter_btn = gr.Button("Apply Categorical Filter", variant="primary", size="sm")
                    
                    # Date Filter Section
                    gr.Markdown("**Date Filter (Date Range)**")
                    with gr.Row():
                        date_start = gr.Textbox(
                            label="Start Date (YYYY-MM-DD)",
                            placeholder="2024-01-01",
                            interactive=True
                        )
                        date_end = gr.Textbox(
                            label="End Date (YYYY-MM-DD)",
                            placeholder="2024-12-31",
                            interactive=True
                        )
                    apply_date_filter_btn = gr.Button("Apply Date Filter", variant="primary", size="sm")
                    
                    # Filter Management
                    gr.Markdown("### Manage Filter")
                    clear_filter_btn = gr.Button("Clear Current Filter", variant="secondary", size="sm")
                
                # Right Panel: Results Display
                with gr.Column(scale=2):
                    gr.Markdown("### Filtered Data Results")
                    
                    # Row count indicators
                    with gr.Row():
                        total_row_count = gr.Textbox(
                            label="Total Rows",
                            value="0",
                            interactive=False
                        )
                        filtered_row_count = gr.Textbox(
                            label="Filtered Rows",
                            value="0",
                            interactive=False
                        )
                    
                    # Filtered data preview
                    filtered_data_display = gr.Dataframe(
                        label="Filtered Data Preview (First 100 rows)",
                        interactive=False,
                        wrap=True
                    )
            
            # ============================================================
            # FILTER EVENT HANDLERS
            # ============================================================
            
            # Update filter options when data is loaded
            df_state.change(
                fn=update_filter_options,
                inputs=[df_state],
                outputs=[filter_column_select, total_row_count, filtered_row_count, 
                        filtered_data_display, category_dropdown]
            )
            
            # Update input fields when column is selected
            filter_column_select.change(
                fn=update_inputs_for_column,
                inputs=[df_state, filter_column_select],
                outputs=[numeric_min_input, numeric_max_input, category_dropdown, 
                        date_start, date_end]
            )
            
            # Apply numeric filter
            apply_numeric_filter_btn.click(
                fn=add_numeric_filter_to_state,
                inputs=[df_state, filter_column_select, numeric_min_input, numeric_max_input],
                outputs=[current_filter, filtered_data_display, filtered_row_count]
            )
            
            # Apply categorical filter
            apply_categorical_filter_btn.click(
                fn=add_categorical_filter_to_state,
                inputs=[df_state, filter_column_select, category_dropdown],
                outputs=[current_filter, filtered_data_display, filtered_row_count]
            )
            
            # Apply date filter
            apply_date_filter_btn.click(
                fn=add_date_filter_to_state,
                inputs=[df_state, filter_column_select, date_start, date_end],
                outputs=[current_filter, filtered_data_display, filtered_row_count]
            )
            
            # Clear current filter
            clear_filter_btn.click(
                fn=clear_current_filter,
                inputs=[df_state],
                outputs=[current_filter, filtered_data_display, filtered_row_count]
            )
        
        with gr.Tab("Visualizations"):
            gr.Markdown("## Data Visualizations")
            gr.Markdown("### Create various charts to explore your data visually")
            
            with gr.Tabs():
                # Time Series Plot
                with gr.Tab("Time Series"):
                    gr.Markdown("**Visualize trends over time**")
                    with gr.Row():
                        with gr.Column(scale=1):
                            ts_date_col = gr.Dropdown(label="Date Column", choices=[])
                            ts_value_col = gr.Dropdown(label="Value Column", choices=[])
                            ts_agg_method = gr.Dropdown(
                                label="Aggregation Method",
                                choices=["sum", "mean", "count", "median", "min", "max"],
                                value="sum"
                            )
                            ts_plot_btn = gr.Button("Generate Time Series Plot", variant="primary")
                        with gr.Column(scale=2):
                            ts_plot_output = gr.Plot(label="Time Series Plot")
                            # ts_export_btn = gr.Button("Export as PNG", size="sm")
                
                # Distribution Plot
                with gr.Tab("Distribution"):
                    gr.Markdown("**Analyze distribution of numerical data**")
                    with gr.Row():
                        with gr.Column(scale=1):
                            dist_col = gr.Dropdown(label="Numeric Column", choices=[])
                            dist_type = gr.Radio(
                                label="Plot Type",
                                choices=["Histogram", "Box Plot"],
                                value="Histogram"
                            )
                            dist_plot_btn = gr.Button("Generate Distribution Plot", variant="primary")
                        with gr.Column(scale=2):
                            dist_plot_output = gr.Plot(label="Distribution Plot")
                            # dist_export_btn = gr.Button("Export as PNG", size="sm")
                
                # Category Analysis
                with gr.Tab("Category Analysis"):
                    gr.Markdown("**Analyze categorical data**")
                    with gr.Row():
                        with gr.Column(scale=1):
                            cat_col = gr.Dropdown(label="Categorical Column", choices=[])
                            cat_value_col = gr.Dropdown(label="Value Column (Optional)", choices=[])
                            cat_type = gr.Radio(
                                label="Chart Type",
                                choices=["Bar Chart", "Pie Chart"],
                                value="Bar Chart"
                            )
                            cat_plot_btn = gr.Button("Generate Category Plot", variant="primary")
                        with gr.Column(scale=2):
                            cat_plot_output = gr.Plot(label="Category Plot")
                            # cat_export_btn = gr.Button("Export as PNG", size="sm")
                
                # Scatter Plot / Correlation
                with gr.Tab("Relationships"):
                    gr.Markdown("**Explore relationships between variables**")
                    with gr.Row():
                        with gr.Column(scale=1):
                            rel_type = gr.Radio(
                                label="Analysis Type",
                                choices=["Scatter Plot", "Correlation Heatmap"],
                                value="Scatter Plot"
                            )
                            scatter_x_col = gr.Dropdown(label="X-Axis Column", choices=[])
                            scatter_y_col = gr.Dropdown(label="Y-Axis Column", choices=[])
                            rel_plot_btn = gr.Button("Generate Plot", variant="primary")
                        with gr.Column(scale=2):
                            rel_plot_output = gr.Plot(label="Relationship Plot")
                            # rel_export_btn = gr.Button("Export as PNG", size="sm")
            
            # Update dropdowns when data is loaded
            df_state.change(
                fn=lambda data: update_visualization_options(data),
                inputs=[df_state],
                outputs=[ts_date_col, ts_value_col, dist_col, cat_col, cat_value_col, 
                        scatter_x_col, scatter_y_col]
            )
            
            # Time Series Plot Events
            ts_plot_btn.click(
                fn=visualization.time_series_plot,
                inputs=[df_state, ts_date_col, ts_value_col, ts_agg_method],
                outputs=[ts_plot_output]
            )
            
            # ts_export_btn.click(
            #     fn=visualization.export_plot_as_png,
            #     inputs=[ts_plot_output],
            #     outputs=[gr.File(label="Download PNG")]
            # )
            
            # Distribution Plot Events
            dist_plot_btn.click(
                fn=visualization.distribution_plot,
                inputs=[df_state, dist_col, dist_type],
                outputs=[dist_plot_output]
            )
            
            # dist_export_btn.click(
            #     fn=visualization.export_plot_as_png,
            #     inputs=[dist_plot_output],
            #     outputs=[gr.File(label="Download PNG")]
            # )
            
            # Category Plot Events
            cat_plot_btn.click(
                fn=visualization.category_analysis_plot,
                inputs=[df_state, cat_col, cat_value_col, cat_type],
                outputs=[cat_plot_output]
            )
            
            # cat_export_btn.click(
            #     fn=visualization.export_plot_as_png,
            #     inputs=[cat_plot_output],
            #     outputs=[gr.File(label="Download PNG")]
            # )
            
            # Relationship Plot Events
            rel_plot_btn.click(
                fn=visualization.relationship_plot,
                inputs=[df_state, rel_type, scatter_x_col, scatter_y_col],
                outputs=[rel_plot_output]
            )
            
            # rel_export_btn.click(
            #     fn=visualization.export_plot_as_png,
            #     inputs=[rel_plot_output],
            #     outputs=[gr.File(label="Download PNG")]
            # )
        
        with gr.Tab("Insights"):
            gr.Markdown("## Automated Insights")
            gr.Markdown("### Discover patterns, trends, and anomalies in your data")
            
            insights_btn = gr.Button("Generate Insights", variant="primary")
            
            with gr.Row():
                with gr.Column():
                    performers_output = gr.Markdown(label="Top/Bottom Performers")
                with gr.Column():
                    trends_output = gr.Markdown(label="Trends and Anomalies")
            
            insights_btn.click(
                fn=insights.generate_all_insights,
                inputs=[df_state],
                outputs=[performers_output, trends_output]
            )
    
    return demo

if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(theme=gr.themes.Soft())
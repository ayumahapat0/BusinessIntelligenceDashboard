import gradio as gr
import pandas as pd
import data_processor

"""
This is the gradio interface
for the Business Intelligence Dashboard.
"""

def create_dashboard():
    with gr.Blocks() as demo:
        gr.Markdown("# Business Intelligence Dashboard")
        
        df_state = gr.State(None)  # To hold the DataFrame across tabs

        def load_data(file_input):
            """
            Load and clean data using data_processor module.
            
            Args:
                file_input: Uploaded file object from Gradio.
            Returns:
                data: Cleaned pandas DataFrame or None if there are any errors
                string: Status message regarding the data loading process.
            """
            
            data, string = data_processor.load_clean_data(file_input)
            
            if data is None:
                return data, string
            
            return data, "Data loaded successfully."
        
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
                        outputs = [df_state, gr.Textbox(label="Upload Status", lines=2)],
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
            # Summary statistics and profiling
            pass
        
        with gr.Tab("Filter & Explore"):
            # Interactive filtering
            pass
        
        with gr.Tab("Visualizations"):
            # Charts and graphs
            pass
        
        with gr.Tab("Insights"):
            # Automated insights
            pass
    
    return demo

if __name__ == "__main__":
    demo = create_dashboard()
    demo.launch(theme=gr.themes.Soft())
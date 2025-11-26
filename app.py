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
            data = data_processor.load_clean_data(file_input)
            return data
        
        def display_data_info(data):
            info = data_processor.get_data_info(data)
            if info:
                num_rows, num_cols, col_names, data_types = info
                return f"Rows: {num_rows}, Columns: {num_cols}, Column Names: {col_names}, Data Types: {data_types}"
            else:
                return "No data loaded."
        
        def preview_data_fn(data, num_rows, first, last):
            first, last = data_processor.preview_data(data, num_rows=num_rows, first=True, last=True)
            return first, last
        
        with gr.Tab("Data Upload"):
            
            # File upload
            upload_btn = gr.Button("Upload Data File")
            file_input = gr.File(label="Upload CSV or Excel File")
            upload_btn.click(
                fn = load_data,
                inputs = [file_input],
                outputs = [df_state]
            )

            # Display Data info
            data_info_output = gr.Textbox(label="Data Information")
            data_preview_btn = gr.Button("Display Data Info")
            data_preview_btn.click(
                fn = display_data_info,
                inputs = [df_state],
                outputs = [data_info_output]
            )

            # Data Preview
            num_rows_input = gr.Slider(5, 25, value=5, label="Number of Rows to Preview")
            first_rows_preview = gr.Dataframe(label="First Rows Preview")
            last_rows_preview = gr.Dataframe(label="Last Rows Preview")

            # First rows checkbox
            first_checkbox = gr.Checkbox(label="Show First Rows", value=True)

            # Last rows checkbox
            last_checkbox = gr.Checkbox(label="Show Last Rows", value=False)
            data_preview_btn = gr.Button("Preview Data")
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
    demo.launch()
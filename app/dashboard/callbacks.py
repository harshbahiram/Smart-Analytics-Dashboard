import base64
import io
import os
from datetime import datetime
import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from app.analytics.charts import generate_charts

from app.analytics.profiler import generate_profile

UPLOAD_FOLDER = "app/uploads"

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded  = base64.b64decode(content_string)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    saved_filename = f"{timestamp}_{filename}"

    filepath = os.path.join(UPLOAD_FOLDER, saved_filename)

    try:
        with open(filepath, "wb") as f:
            f.write(decoded)

        if filename.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        else:
            return html.Div([
                'Unsupported file format. Please upload a CSV or Excel file.'
            ])
        
        profile = generate_profile(df)

        charts = generate_charts(df)

        info = html.Div([

            html.H3("Dataset Information"),

            html.P(f"Filename: {saved_filename}"),
            html.P(f"Rows: {profile['rows']}"),
            html.P(f"Columns: {profile['columns']}"),

            html.Hr(),

            html.H3("Data Quality Report"),

            html.P(f"Missing Values: {profile['missing_values']}"),
            html.P(f"Duplicate Rows: {profile['duplicate_rows']}"),
            html.P(f"Numeric Columns: {profile['numeric_columns']}"),

            html.P(
                f"Categorical Columns: "
                f"{profile['categorical_columns']}"
            )

        ])

        table = dash_table.DataTable(
            data=df.head(10).to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={'overflowX': 'auto'},
            page_size=10
        )
        return info, html.Div([
            table,
            html.Hr(),
            html.H2("Auto Generated Charts"),
            *charts
        ])
    
    except Exception as e:  
        return html.Div([
            f"Error processing file: {str(e)}"
        ])
    
def register_callbacks(app):

    @app.callback(
        [
            Output('dataset-info', 'children'),
            Output('output-data-upload', 'children')
        ],
        Input('upload-data', 'contents'),
        State('upload-data', 'filename')
    )

    def update_output(contents, filename):
        if contents is not None:
            return parse_contents(contents, filename)
        return "",""
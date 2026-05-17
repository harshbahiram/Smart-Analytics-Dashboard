import base64
import io
import os
from datetime import datetime
import pandas as pd
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from app.analytics.charts import (generate_charts, generate_heatmap)
from app.analytics.profiler import generate_profile
from app.analytics.analytics import generate_insights

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
        heatmap = generate_heatmap(df)
        insights = generate_insights(
            df,
            profile
        )
        info = html.Div([

            html.H3("Dataset Information"),

            html.P(f"Filename: {saved_filename}"),
            html.P(f"Rows: {profile['rows']}"),
            html.P(f"Columns: {profile['columns']}"),

            html.Hr(),

            html.H3("Data Quality Report"),

            html.H4("Missing Values Details"),
            html.Ul([
                html.Li(
                    f"{col}: "
                    f"{profile['missing_per_column'][col]} missing "
                    f"({profile['missing_percentage'][col]}%)"
                )
                for col in profile['missing_per_column']
                if profile['missing_per_column'][col] > 0
            ]),

            html.H4("Unique Values per Column"),
            html.Ul([
                html.Li(
                    f"{col}: "
                    f"{profile['unique_values'][col]} unique values"
                )
                for col in profile['unique_values']
            ]),


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
            *charts,
            html.Hr(),
            html.H2("Correlation Analysis"),
            html.Hr(),
            html.H2("Smart Insights"),
            html.Ul([
                html.Li(insight) for insight in insights
            ]),
            heatmap
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
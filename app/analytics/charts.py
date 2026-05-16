import plotly.express as px
from dash import dcc, html

def generate_charts(df):

    charts = []

    numeric_columns = df.select_dtypes(include=['number']).columns
    categorical_columns = df.select_dtypes(include=['object']).columns

    for col in numeric_columns:
        fig = px.histogram(
            df, x=col, title=f"Distribution of {col}"
        )

        charts.append(
            html.Div([
                dcc.Graph(figure=fig)
            ], 
            style={'marginBottom': '40px'}
            )
        )

    for col in categorical_columns:

        value_counts = df[col].value_counts().head(10)

        fig = px.bar(
            x = value_counts.index, 
            y=value_counts.values, 
            
            labels = {
                'x': col, 
                'y': "Count"
            },
            title=f"{col} Distribution"
        )
        charts.append(
            html.Div([
                dcc.Graph(figure=fig)
            ], 
            style={'marginBottom': '40px'}
            )
        )
    return charts
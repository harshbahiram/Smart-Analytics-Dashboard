import plotly.express as px
from dash import dcc, html


def generate_charts(df):
    """Generate charts based on column data types."""
    charts = []

    numeric_columns = df.select_dtypes(include=["number"]).columns
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for col in numeric_columns:
        fig = px.histogram(
            df, x=col, title=f"Distribution of {col}"
        )

        charts.append(
            html.Div(
                dcc.Graph(figure=fig),
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


def generate_heatmap(df):
    """Generate correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.shape[1] < 2:

        return html.Div([
            html.H3(
                "Not enough numeric columns for correlation heatmap"
            )
        ])
    
    correlation_matrix = numeric_df.corr().round(2)

    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )

    return html.Div([
        dcc.Graph(figure=fig)
    ])
from dash import html, dcc, dash_table

layout = html.Div([
    html.H1("Smart Analytics Dashboard",
    style={
    "textAlign": "center",
    "marginBottom": "30px"
    }),

    # To create a file upload component
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '60%',
            'height': '80px',
            'lineHeight': '80px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': 'auto',
            'marginBottom': '30px'
        },
        multiple=False
    ),

    html.Div(id='dataset-info'), # show dataset info after upload
    html.Div(id='output-data-upload') # show data preview after upload

])
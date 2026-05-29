from dash import html, dcc

layout = html.Div(

    className="main-container",

    children=[

        html.Div([

            html.H1(
                "📊 Smart Analytics Dashboard"
            ),

            html.P(
                "Upload CSV / Excel and generate analytics automatically"
            )

        ],

        className="header"),

        html.Div([

            dcc.Upload(

                id="upload-data",

                children=html.Div([
                    "Drag & Drop or Select CSV / Excel File"
                ]),

                style={
                    "width":"100%",
                    "height":"80px",
                    "lineHeight":"80px",
                    "borderWidth":"2px",
                    "borderStyle":"dashed",
                    "borderRadius":"10px",
                    "textAlign":"center"
                }

            )

        ],

        className="card"),

        html.Div(
            id="dataset-info"
        ),

        html.Div(
            id="output-data-upload"
        )

    ])
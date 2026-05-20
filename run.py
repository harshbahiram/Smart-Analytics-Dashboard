import os
import sys

from flask import Flask
from dash import Dash

from app.dashboard.layout import layout
from app.dashboard.callbacks import register_callbacks
from app.database.db import engine
from app.database.models import Base


server = Flask(__name__)

app = Dash(
    __name__,
    server=server,
    assets_folder="app/static"
)

app.layout = layout

register_callbacks(app)

Base.metadata.create_all(
    bind=engine
)

if __name__ == "__main__":
    app.run(debug=True)
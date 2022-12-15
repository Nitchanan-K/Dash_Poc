import base64
import datetime
import io
import pandas as pd 

from dash import dcc,html

dcc_Upload = dcc.Upload(
    id='upload-data',
    children=html.Div([
            'Drag and Drop or ',
             html.A('Select File')
]),
    style={     
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'},
            # Allow multiple files to be uploaded
            multiple=True
)



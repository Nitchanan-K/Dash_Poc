from dash import Dash, dash_table, dcc, html,no_update 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash()

app.layout = html.Div([
    html.Label('Select a value:'),
    html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Option 1', 'value': '1'},
                {'label': 'Option 2', 'value': '2'},
                {'label': 'Option 3', 'value': '3'},
            ],
            value='1',
        )
    ]),
    html.Div(id='output')
])

@app.callback(
    Output('output', 'children'),
    [Input('dropdown', 'value')])
def update_output(value):
    return f'You selected "{value}"'

if __name__ == '__main__':
    app.run_server(debug=True)
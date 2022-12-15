import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

if __name__ == '__main__':
    app = dash.Dash(__name__,external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

    app.layout = html.Div([
        dcc.Input(id='username', value='Initial Value', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit'),
        html.Div(id='output_div')
    ])

    @app.callback(Output('output_div', 'children'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  )
    def update_output(clicks, input_value):
        if clicks is not None:
            print(input_value)

    app.run_server(debug=True)
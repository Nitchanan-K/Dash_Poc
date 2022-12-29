import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    # Header
    html.Div(children=[
        html.H1(children='My Dash App', style={'color': '#ffffff'}),
        html.Hr()
    ], style={'backgroundColor': '#5f9ea0', 'padding': '20px'}),

    # Body
    html.Div(children=[
        # Sidebar
        html.Div(children=[
            html.H2(children='Sidebar'),
            html.P(children='Sidebar content')
        ], className='bg-light three columns'),

        # Main content
        html.Div(children=[
            html.H2(children='Main content'),
            html.P(children='Main content goes here')
        ], className='nine columns')
    ], className='row')
])

if __name__ == '__main__':
    app.run_server(debug=True)
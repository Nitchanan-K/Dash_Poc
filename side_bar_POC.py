import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

import plotly.express as px

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa"
}


sidebar = html.Div([
    html.H2("Sidebar"),
    html.P("This is the sidebar"),
    dcc.Link("Link 1", href="/link1"),
    html.Br(),
    dcc.Link("Link 2", href="/link3")    
                    ])
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
from Components.input_set_cash import dcc_Cash_Input
trade_setup = 
    # SET STRATEGY 
    dcc.Dropdown(['Sma4Cross','SmaCross','3'],'Sma4Cross', id='demo-dropdown'),
    html.Div(id='dd-output-container'),

    # SET CASH
    dcc_Cash_Input,
    html.Button(id='submit-button', type='submit', children='Submit'),
    html.Div(id='output_div_BUTTON'),

    # SET COMMISSION AND MARGIN
    dcc.Input(id='set_commission', value=0.0, type="number",placeholder='Set Comission',
    debounce= True,min=0,minLength=0,maxLength=10,required=False,step=0.0001),
    html.Br(),
    dcc.Input(id='set_margin', value=1, type="number",placeholder='Set Margin',
    debounce= True,min=0,minLength=0,maxLength=10,required=False,step=0.01),

    # Confirm Button
    dcc.ConfirmDialogProvider(
        children=html.Button(id='confirm-button', children='Confrim Setup',type='submit'),
        id='danger-provider',
        message='Confirm Trade Setup?',
        submit_n_clicks=0
    ),
    html.Div(id='output-confirm-button'),


    # SET BOOLEAN OF trade on close / hedging / exclusive order 
    # trade on close 
    daq.BooleanSwitch(id='trade_on_close_boolean_switch', on=False),
    html.Div(id='trade_on_close_boolean_output'),
    # hedging
    daq.BooleanSwitch(id='hedging_boolean_switch', on=False),
    html.Div(id='hedging_boolean_output'),
    # exclusive order 
    daq.BooleanSwitch(id='exclusive_order_boolean_switch', on=False),
    html.Div(id='exclusive_order_boolean_output')

 

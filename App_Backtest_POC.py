import base64
import datetime
import io

import dash
from dash import Dash, dcc, Output, Input, State , html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd 

from backtesting import Backtest , Strategy
# import strategy cless
import strategy_class.SmaCross_class
# initiate strategy class
SmaCross = strategy_class.SmaCross_class.SmaCross

# Import dcc_component 
from select_file import dcc_upload

# INCORPRORATE DATA INTO APP
# index = Date , Parse_dates = True 
df = pd.read_csv('eth.csv', index_col='Date',parse_dates=True)


# Bulid Components
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
title = dcc.Markdown(children='')
#backtest_result = 
button = dbc.Button("Confrim", color="primary", id="example-button", className="me-1", n_clicks=0)
span = html.Span(id="example-output", style={"verticalAlign": "middle"})
# show data file (component)


# APP Layout 
app.layout = html.Div(
    [dcc_upload,
    button,
    span,
    html.Div(id='output-data-upload')
    ]
)

# Function 
def get_data_content(file):
    try:
        if 'csv' in file:
            df_content = pd.read_csv(file, index_col='Date',parse_dates=True)
            print(df_content)
        elif 'xls' in file:
            df_content = pd.read_excel(file,index_col='Date',parse_dates=True)
    except Exception as e:
        print(e)
    return df_content

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=";")
            #parse_contents.df_content = df
            #get_data_content(df)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
           
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    # RETURN TABLE
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


# CallBack 
@app.callback(
    Output("example-output", component_property="children"),
    Input("example-button",component_property="n_clicks")
)


def on_button_click(n):
    if n:
        print(1)
        bt = Backtest(df, SmaCross, cash=1000000, commission=0.02,margin=1,hedging=False,
        trade_on_close=False,exclusive_orders=False)
        print(SmaCross)
        stats = bt.run()
        print(stats)
        bt.plot()
        return f"Clicked {n} times."
    else:
        pass

# fix bug float is not iterable https://stackoverflow.com/questions/74145275/float-object-not-iterable-dcc-upload-in-dash
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children



# Run APP
if __name__ == '__main__':
    app.run_server(debug= True, port=8051)
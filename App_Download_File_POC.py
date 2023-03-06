import base64
import datetime
import io
from datetime import date

import dash
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px

import pandas as pd

# import yahoo API 
from yahoo_fin.stock_info import *
from yahoo_fin.stock_info import get_analysts_info
import yahoo_fin.stock_info as si

'''
data_downloaded = get_data('BTC-USD',start_date='01/01/2020',end_date='01/01/2021', index_as_date=False,
interval='1d')

df = pd.DataFrame(data_downloaded)
df.drop(columns='ticker', inplace=True)
df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                       'adjclose': 'Adjclose', 'volume': 'Volume'}, inplace=True)

df.reset_index(drop=True, inplace=True)

#print(df)
'''


app = Dash(__name__)
app.layout = html.Div([
 
    dcc.DatePickerRange
    (
        id='my-date-picker-range',
        min_date_allowed=date(2008,12,30),
        max_date_allowed=date(2030,1,1),
        initial_visible_month=date(2022,1,1),
        end_date=date(2017, 8, 25)
        
    ),
    html.Hr(),
    html.Div(id='output-container-date-picker-range'),
    html.Hr(),
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv")
])

#  APP CALLBACK -- DOWNLOAD DATAFRAME CSV SECTION 
#  APP CALLBACK (DOWNLOAD DATA API)
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date'),
    prevent_initial_call=True,
)
def func(n_clicks,start_date, end_date):
   
    if n_clicks is not None:
        print(n_clicks)
    
        if start_date and end_date is not None:
            start_date_object = date.fromisoformat(start_date)
            start_date_string = start_date_object.strftime('%m/%d/%Y')
            #print(start_date_string)

            end_date_object = date.fromisoformat(end_date)
            end_date_string = end_date_object.strftime('%m/%d/%Y')
            #print(end_date_string)


        # download data from API yahoo fin 
        data_downloaded = get_data('BTC-USD',start_date=start_date_string,
                                             end_date=end_date_string, 
                                             index_as_date=False,
                                             interval='1d')

        
        # clearing data 
        df = pd.DataFrame(data_downloaded)
        df.drop(columns='ticker', inplace=True)
        df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                       'adjclose': 'Adjclose', 'volume': 'Volume'}, inplace=True)
        df.reset_index(drop=True, inplace=True)

    return dcc.send_data_frame(df.to_csv, 'mydf.csv')


#  APP CALLBACK (DATE PICK RANGE)
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_output_start_end_date(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

if __name__ == "__main__":
    app.run_server(debug=True)


import base64
import datetime
import io

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

data_downloaded = get_data('BTC-USD',start_date='01/01/2020',end_date='01/01/2021', index_as_date=False,
interval='1d')

df = pd.DataFrame(data_downloaded)
df.drop(columns='ticker', inplace=True)
df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                       'adjclose': 'Adjclose', 'volume': 'Volume'}, inplace=True)

df.reset_index(drop=True, inplace=True)


print(df)

app = Dash(__name__)
app.layout = html.Div([
    html.Button("Download CSV", id="btn_csv"),
    dcc.Download(id="download-dataframe-csv")
])


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df.to_csv, 'mydf.csv')


if __name__ == "__main__":
    app.run_server(debug=True)


import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table,
import dash_bootstrap_components as dbc

import plotly.express as px

import pandas as pd
# -----------------
# Backtest lib 
from backtesting import Backtest , Strategy
# import strategy cless
import strategy_class.SmaCross_class
# initiate strategy class
SmaCross = strategy_class.SmaCross_class.SmaCross
# -----------------
# IMPORT COMPONENTS 
from Components.upload_data_component import dcc_Upload
from Components.input_set_cash import ddc_Cash_Input



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('test_data.csv',index_col='Date',parse_dates=True)


app = dash.Dash(__name__,external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True)

app.layout = html.Div([
    # SET CASH
    ddc_Cash_Input,
    html.Button(id='submit-button', type='submit', children='Submit'),
    html.Div(id='output_div_BUTTON'),
    # SET COMMISSION AND MARGIN
    dcc.Input(id='set_commission', value=0.0, type="number",placeholder='Set Comission',
    debounce= True,min=0,minLength=0,maxLength=10,required=False,step=0.0001),
    html.Br(),
    dcc.Input(id='set_margin', value=1, type="number",placeholder='Set Margin',
    debounce= True,min=0,minLength=0,maxLength=10,required=False,step=0.01),
    # SET BOOLEAN OF trade on close / hedging / exclusive order 
    dcc.Checklist(
        id='trade_on_close',
        options=[
                {'lable':'test'}
        ],value="test trade"),

    # UPLOAD FILE USE AS DATA
    dcc_Upload,
    # Will show when data is uploaded ------
    html.Div(id='output-div'),
    html.Div(id='output-div-backtest'),
    html.Div(id='output-datatable'),

    ])

# FUNCTION ------------------------------------------

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.P("Inset X axis data"),
        dcc.Dropdown(id='xaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.P("Inset Y axis data"),
        dcc.Dropdown(id='yaxis-data',
                     options=[{'label':x, 'value':x} for x in df.columns]),
        html.Button(id="submit-button_PLOT_GRAPH", children="Create Graph"),
        html.Button(id="plot-button", children="Plot"),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=15
        ),
        # file size no more than 2-5 mb
        dcc.Store(id='stored-data', data=df.to_dict('records')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

# CALLBACK ------------------------------------------
# APP CALLBACK (UPLOAD DATA)
@app.callback(Output('output-datatable', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

# APP CALLBACK (PLOT GRAPHS)
@app.callback(Output('output-div', 'children'),
              Input('submit-button_PLOT_GRAPH','n_clicks'),
              State('stored-data','data'),
              State('xaxis-data','value'),
              State('yaxis-data', 'value'))

def make_graphs(n, data, x_data, y_data):
    # set up data 
    df = pd.DataFrame(data,columns=['Date','Open','High','Low','Close','Adjclose','Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    print("set up data  done (def make_graphs)")
    
    if n is None:
    
        return dash.no_update
    else:
        # Plot graphs 
        print("def make graphs working 2 ")
        #print(df)
        bar_fig = px.bar(data, x=x_data, y=y_data)
        return dcc.Graph(figure=bar_fig)

# APP CALLBACK (PLOT BACKTEST)
@app.callback(Output('output-div-backtest','children'), # OUTPUT TO 'output-div-backtest' div
              Input('plot-button','n_clicks'), # WILL PLOT WHEN BUTTON ID = 'plot_button' is clicks
              State('stored-data','data'),
              State('set_cash','value'),
              State('set_commission','value'),
              State('set_margin','value')
              )


def plot_backtest(n,data,num_set_cash,num_set_commission,num_set_margin):
    # set up data 
    df = pd.DataFrame(data,columns=['Date','Open','High','Low','Close','Adjclose','Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    print("set up data  done (plot_backtest)")
    
    # set variables for backtest 
    cash_from_input = num_set_cash
    commission_from_input = num_set_commission
    margin_from_input = num_set_margin

    if n is not None:
        print("BUTTON CLICKED (plot_backtest)")
        #print(df)

        # SET UP BACKTEST 
        bt = Backtest(df, SmaCross, cash=cash_from_input, 
        commission=commission_from_input,margin=margin_from_input,hedging=False,
        trade_on_close=False,exclusive_orders=False)
        # PLOT BACKTEST 
        stats = bt.run()
        #print(stats)
        bt.plot()

        # check input passed from user 
        print('cash =', cash_from_input)
        print('commission', commission_from_input)
        print('margin',margin_from_input)
    else:
        return dash.no_update





# TEXT INPUT 
@app.callback(Output('output_div_BUTTON', 'children'),
                [Input('submit-button', 'n_clicks')],
                [State('set_cash', 'value')],
                )
def update_output(clicks, input_value):
    var = input_value
    if clicks is not None:
        print(var)
    return var



if __name__ == '__main__':
    app.run_server(debug=True)
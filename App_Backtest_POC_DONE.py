import base64
import datetime
import io
from datetime import date

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px

import pandas as pd
# -----------------
# Backtest lib 
from backtesting import Backtest , Strategy
# IMPORT Strategy Cless
import strategy_class.SmaCross_class,strategy_class.Sma4Cross_class
# initiate strategy class
SmaCross = strategy_class.SmaCross_class.SmaCross
Sma4Cross = strategy_class.Sma4Cross_class.Sma4Cross
# -----------------
# IMPORT COMPONENTS 
from Components.upload_data_component import dcc_Upload
from Components.input_set_cash import dcc_Cash_Input
# -----------------
# IMPORT yahoo API 
from yahoo_fin.stock_info import *
from yahoo_fin.stock_info import get_analysts_info
import yahoo_fin.stock_info as si

# set dict strategy use in drop down string 
strategy_dict = {'SmaCross':SmaCross,'Sma4Cross':Sma4Cross}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#df = pd.read_csv('test_data.csv',index_col='Date',parse_dates=True)


app = dash.Dash(__name__,external_stylesheets=external_stylesheets,
            suppress_callback_exceptions=True)

app.layout = html.Div(
    id="app-container",
    children=
    [
        # Left column
        html.Div(
            id="left-column",
            className="eight columns",
            children=[
    
            # SET STRATEGY 
            html.P("Select Your Strategy"),
            dcc.Dropdown(['Sma4Cross','SmaCross','3'],'Sma4Cross', id='demo-dropdown'),
            html.Div(id='dd-output-container'),
            html.Br(),

            # SET CASH
            html.P("Set Your Innitial Cash"),
            dcc_Cash_Input,
            html.Button(id='submit-button', type='submit', children='Submit'),
            html.Div(id='output_div_BUTTON'),
            html.Br(),
    
            # SET COMMISSION AND MARGIN
            html.P("Set Your Commission %"),
            dcc.Input(id='set_commission', value=0.0, type="number",placeholder='Set Comission',
            debounce= True,min=0,minLength=0,maxLength=10,required=False,step=0.0001),
            html.Br(),
            html.P("Set Your Margin"),
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
            html.Div(id='exclusive_order_boolean_output'),

            # UPLOAD FILE USE AS DATA
            dcc_Upload,

            # Will show when data is uploaded ------
            html.Div(id='output-div'),
            html.Div(id='output-div-backtest'),
            html.Div(id='output-datatable'),
           
            # END Left Column
            
            # html.Iframe(src='Sma4Cross.html', style={'width': '100%', 'height': 500}) = making bugs with multiple windows showing
              # Right column
            html.Div(id='right-column',
                     className='three columns',
                     children=[
                                    # TEXT INPUT
                                    html.P("For example BTC-USD or ETH-USD"),
                                    dcc.Input(id="ticket_input",type='text', value='',placeholder='Crypto Name'),
                                    html.Div(id='ticket_output'),
                                

                                    dcc.DatePickerRange
                                    (   id='my-date-picker-range',
                                        min_date_allowed=date(2008,12,30),
                                        max_date_allowed=date(2030,1,1),
                                        initial_visible_month=date(2022,1,1),
                                        end_date=date(2017, 8, 25) 
                                    ),

                                    html.Hr(),
                                    html.Div(id='output-container-date-picker-range'),
                                    html.Hr(),

                                    dcc.Dropdown(['Day','Week','Month'],'Day',id='interval-dropdown'),
                                    html.Div(id='dd-interval-output-container'),

                                    html.Button("Download CSV", id="btn_csv"),
                                    html.Hr(),
                                    dcc.Download(id="download-dataframe-csv")
                              ]
                 
                 
                     )
                    ])
                # END RIGHT Column
            
      
                 

    ])
    # END app.layout

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

        # horizontal line
        html.Hr()
        ,  
        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



# CALLBACK ------------------------------------------ LEFT COLUMN

# APP CALLBACK (DROP DOWN)
@app.callback(
    Output('dd-output-container','children'),
    Input('demo-dropdown', 'value')
)
def update_output_dropdown(value):
    return f'You have selected {value} strategy'

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

# APP CALLBACK (BOOLEAN SWITCH)
# (trade_on_close)
@app.callback(
            Output('trade_on_close_boolean_output', 'children'),
            Input('trade_on_close_boolean_switch', 'on')
)
def update_output_trade_on_close_switch(on):
    return f'Trade On Close : {on}.'

# (hedging)
@app.callback(
    Output('hedging_boolean_output', 'children'),
    Input('hedging_boolean_switch', 'on')
)
def update_output_hedging_switch(on):
    return f'Hedging : {on}.'

# (exclusive_order)
@app.callback(
    Output('exclusive_order_boolean_output', 'children'),
    Input('exclusive_order_boolean_switch', 'on')
)
def update_output_exclusive_order_switch(on):
    return f'Exclusive Order: {on}.'

# APP CALLBACK (PLOT BACKTEST)
@app.callback(Output('output-div-backtest','children'), # OUTPUT TO 'output-div-backtest' div
              Input('plot-button','n_clicks'), # WILL PLOT WHEN BUTTON ID = 'plot_button' is clicks
              State('stored-data','data'),
              State('set_cash','value'),
              State('set_commission','value'),
              State('set_margin','value'),
              State('trade_on_close_boolean_switch','on'),
              State('hedging_boolean_switch','on'),
              State('exclusive_order_boolean_switch','on'),
              State('demo-dropdown','value')
              )


def plot_backtest(n,data,num_set_cash,num_set_commission,num_set_margin,boolean_set_trade_on_close,
boolean_set_hedging,boolean_set_exclusive_order,str_set_strategy):
    # set up data 
    df = pd.DataFrame(data,columns=['Date','Open','High','Low','Close','Adjclose','Volume'])
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    print("set up data done (plot_backtest)")
    
    # set variables for backtest 
    cash_from_input = num_set_cash
    commission_from_input = num_set_commission
    margin_from_input = num_set_margin
    trade_on_close_from_input = boolean_set_trade_on_close
    hedging_from_input = boolean_set_hedging
    exclusive_order_from_input = boolean_set_exclusive_order
    strategy_from_input = strategy_dict[str_set_strategy]

    if n is not None:
        print("BUTTON CLICKED (plot_backtest)")
        
        # SET UP BACKTEST 
        bt = Backtest(df, 
        strategy_from_input, 
        cash=cash_from_input, 
        commission=commission_from_input,
        margin=margin_from_input,
        hedging=hedging_from_input,
        trade_on_close=trade_on_close_from_input,
        exclusive_orders=exclusive_order_from_input)

        # PLOT BACKTEST 
        stats = bt.run()
        #print(stats)
        bt.plot()

        # check input passed from user 
        print('cash =', cash_from_input)
        print('commission =', commission_from_input)
        print('margin =',margin_from_input)
        print('trade_on_close =',trade_on_close_from_input)
        print('hedgin =',hedging_from_input)
        print('exclusive_orders =',exclusive_order_from_input)
        print('strategy =',strategy_from_input)
    else:
        return dash.no_update



# APP CALLBACK (TEXT INPUT)
@app.callback(
    Output('output_div_BUTTON', 'children'),
                [Input('submit-button', 'n_clicks')],
                [State('set_cash', 'value')]
                
                )
def update_output(clicks, input_value):
    var = input_value
    if clicks is not None:
        print(var)
    return var," USD"

# APP CALLBACK (CONFRIM BUTTON) 
@app.callback(
    Output('output-confirm-button','children'),
    [Input('danger-provider', 'submit_n_clicks')],
    [State('set_cash', 'value')],
    [State('set_commission','value')],
    [State('set_margin','value')],
    [State('trade_on_close_boolean_switch','on')],
    [State('hedging_boolean_switch','on')],
    [State('exclusive_order_boolean_switch','on')]
                
)

# CALLBACK ------------------------------------------ RIGHT COLUMN
# APP CALLBACK (TEXT INPUT)
# APP CALLBACK -- DOWNLOAD DATAFRAME CSV SECTION 
# APP CALLBACK (DOWNLOAD DATA API)
@app.callback(
    Output('ticket_output','children'),
    Input('ticket_input', 'value')
)
def text_input(value):
    
    return 'You have entered "{}"'.format(value)


# APP CALLBACK(INTERVAL DROP DOWN)
@app.callback(
    Output('dd-interval-output-container','children'),
    Input('interval-dropdown', 'value')
)
def update_output_dropdown(value):
    return f'You have selected {value} Interval'


#  APP CALLBACK (DOWNLOAD DATA API)
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('my-date-picker-range', 'start_date'),
    State('my-date-picker-range', 'end_date'),
    State('interval-dropdown','value'),
    State('ticket_input','value'),
    prevent_initial_call=True,
)

def func(n_clicks,start_date, end_date,interval,ticket_name):
   
    if n_clicks is not None:
        print(n_clicks)
    
        if start_date and end_date is not None:
            
            # Setup Ticket name
            ticket_name_from_input = ticket_name
            print(ticket_name_from_input)
            # Setup Date
            start_date_object = date.fromisoformat(start_date)
            start_date_string = start_date_object.strftime('%m/%d/%Y')
            print(start_date_string)
            print(type(start_date_string))

            end_date_object = date.fromisoformat(end_date)
            end_date_string = end_date_object.strftime('%m/%d/%Y')
            print(end_date_string)
            print(type(end_date_string))

            # Setup Interval 
            if interval == 'Day':
                interval = '1d'
                print('Interval =',interval)
            elif interval == 'Week':
                interval = '1wk'
                print('Interval =',interval)
            elif interval == 'Month':
                interval = '1mo'
                print('Interval =',interval)

        # download data from API yahoo fin 
        data_downloaded = get_data(f'{ticket_name_from_input}',start_date=start_date_string,
                                             end_date=end_date_string, 
                                             index_as_date=False,
                                             interval=interval)

        
        # clearing data 
        df = pd.DataFrame(data_downloaded)
        df.drop(columns='ticker', inplace=True)
        df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close',
                       'adjclose': 'Adjclose', 'volume': 'Volume'}, inplace=True)
        #df.reset_index(drop=True, inplace=True)
        df.set_index('Date', inplace=True)
    return dcc.send_data_frame(df.to_csv, 'mydf.csv')


#  APP CALLBACK (DATE PICK RANGE)
@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_output(start_date, end_date):
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

###

###


def update_output(clicks,cash,commission,margin,trade_on_close,hedging,exclusive_order):
    if clicks is not None:
        print('--------------','\n','CONFRIM BUTTON Work')
        print(cash,'\n',commission,'\n',margin,'\n',trade_on_close,'\n',hedging,'\n',exclusive_order)
        
    return "cash(usd)=",cash,"commission % ",commission,"margin ",margin,trade_on_close,hedging,exclusive_order

if __name__ == '__main__':
    app.run_server(debug=True)
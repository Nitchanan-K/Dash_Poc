import dash
import pandas as pd
from dash import dash_table as dt
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px

df = pd.DataFrame({'Name' : ['Bob', 'Bob', 'Anna', 'Anna'],
                   'Item' : ['Apple', 'Banana', 'Apple', 'Banana'],
                   'Amount' : [1, 2, 2, 1]})

app = dash.Dash(__name__)

names = df['Name'].unique().tolist()
app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id="filter_dropdown",
            options=[{"label": name, "value": name} for name in names],
            placeholder="-Select a Person-",
            multi=False,
            value=df['Name'].values,
        ),
        dt.DataTable(
            id="table-container",
            columns=[{'name': 'Item', 'id': 'Item', 'presentation':'dropdown'},
                     {'name': 'Amount', 'id': 'Amount'}],
            data=df.to_dict("records"),
            editable=True,
            row_deletable=True,
            dropdown={
                'Item' : {
                    'options': [
                        {'label': i, 'value': i}
                        for i in list(df['Item'].unique())
                        ]
                    }
                }
        ),
        html.Button('Add', id='add_btn', n_clicks = 0),
        dcc.Graph(id='visual')
    ]
)
@app.callback(
    Output("table-container", "data"), 
    Input("filter_dropdown", "value"),
    Input("table-container", "data"),
    Input("table-container", "columns"),
    Input("add_btn", 'n_clicks'))
def display_table(name, rows, columns, n_clicks):
    e = dash.callback_context.triggered[0]['prop_id']
    global df
    if e in ["table-container.data", "table-container.columns"]:
        temp = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        temp['Name'] = name
        df = df[~df['Name'].isin([name])]
        df = df.append(temp)
    elif e == 'add_btn.n_clicks':
        if n_clicks > 0:
            df = df.append(pd.DataFrame({'Name':name, 'Item': '', 'Amount': 0}, index=[0]))
    dff = df[df['Name'].isin([name])].to_dict("records")
    return dff
    
@app.callback(Output('visual', 'figure'),
              Input("table-container", "data"),
              Input("table-container", "columns"))
def display_graph(rows, columns):
    fig = px.bar(df, x='Item', y='Amount')
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
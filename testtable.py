from dash import Dash, dash_table, dcc, html,no_update 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd


df = pd.read_csv('crypto_ticker_list.csv')

app = Dash()

def update_output_div(selected_row_indices):
    if selected_row_indices:
        # Get the data for the selected rows
        selected_rows = df.iloc[selected_row_indices]
        # Update the output div with the selected rows data
        

        return [html.Div(selected_rows.to_html())]
    return [html.Div('No rows selected')]

app.layout = html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        selected_rows=[],
        style_table={
            'maxHeight': '300px',
            'overflowY': 'scroll'
        }
    ),
    html.Div(id='output')
])

@app.callback(
    Output('output', 'children'),
    [Input('table', 'selected_rows')]
)
def display_selected_rows(selected_row_indices):
    print(selected_row_indices)
    
    return update_output_div(selected_row_indices)

if __name__ == '__main__':
    app.run_server()
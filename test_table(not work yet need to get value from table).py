from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd


df = pd.read_csv('crypto_ticker_list.csv')


print({"name": i, "id": i} for i in df.columns)

table = dash_table.DataTable(
        id='datatable-interactivity',
        data = df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        filter_action="native",
        filter_options={"placeholder_text": "Search Name..."},
        page_size=50,
        style_table={'height': '300px', 'overflowY': 'auto'})

app = Dash(__name__)

app.layout = html.Div([ table
    
,
 html.Div(id='datatable-interactivity-container'),
 dbc.Alert(id='tbl_out_1'),
 dbc.Alert(id='tbl_out_2')

])




# CALLBACK


@app.callback(Output('tbl_out_1', 'children'), Input('datatable-interactivity', 'active_cell')
)

def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"

# Define a callback function that retrieves the value of the selected cell
@app.callback(
    Output('tbl_out_2', 'children'),
    [Input('datatable-interactivity', 'selected_cells')]
)
def selected_cell_callback(selected_cells):
    if selected_cells:
        global df
        #column = df['CRYPTO NAME']
        

        cell_value = selected_cells[0]['row']
        row = df.loc[cell_value]
        print(row)
        #print(cell_value)
        return f'Selected cell value: {cell_value}'
    return 'No cell selected'





if __name__ == '__main__':
    app.run_server(debug=True)

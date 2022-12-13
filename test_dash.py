from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px 
import pandas as pd 

# INCORPRORATE DATA INTO APP 
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Good_to_Know/Dash2.0/social_capital.csv")
print(df.head())


# Bulid Components 
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
mytitle = dcc.Markdown(children='')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=df.columns.values[2:],
                        value='Cesarean Delivery Rate', # defult displayed when loads
                        clearable=False)



# Customize Layout 
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([mytitle], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=12)
    ]),
    dbc.Row([
        dbc.Col([dropdown], width=6)
    ], justify='center'),
    ], fluid=True)

# CallBack ( for Interact Components)
@app.callback(
    Output(mygraph, component_property='figure'),
    Output(mytitle, component_property='children'),
    Input(dropdown, component_property='value')
)

def update_graph(column_name): # function arguments come from the component property of the INPUT  

    print(column_name)
    print(type(column_name))

    fig = px.choropleth(data_frame=df,
                        locations='STATE',
                        locationmode="USA-states",
                        scope="usa",
                        height=600,
                        color=column_name,
                        animation_frame='YEAR')


    return fig, '#'+ column_name        # returned objects are assigend to the component property of the Output

# Run APP 
if __name__ == '__main__':
    app.run_server(debug=True ,port=8051)
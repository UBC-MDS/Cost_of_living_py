from dash import Dash, html, dcc, Input, Output, State
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc

data = pd.read_csv("data/processed_data.csv")
cities = sorted(data["city"].unique())
regions = data["region"].unique()
price_subset = ["rent_for_one_person", "transportation_public",
	"grocery_for_one_person", "entertainment", "fitness", "utility_bills",	
    "shopping",	"all", "childcare_for_one_child"]

## THIS IS THE COST COMPARISON PLOT
def plot1(city_name):
    subset = data.loc[data["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.X("city", title = "City"),
         alt.Y("grocery_for_one_person", title = "Grocery Price")
    )
    return chart.to_html()

## THIS IS THE MONTHLY SURPLUS PLOT
def plot2(city_name):
    subset = data.loc[data["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.X("city", title = "City"),
         alt.Y("monthly_saving", title = "Savings")
    )
    return chart.to_html()


## THIS IS THE HEAT MAP PLOT
def plot3(city_name): 
    subset = data.loc[data["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.X("city", title = "City"),
         alt.Y("country", title = "Country")
    )
    return chart.to_html()

## THIS IS THE PROPERTY PRICE PLOT
def plot4(city_name):
    subset = data.loc[data["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.X("city", title = "City"),
         alt.Y("property_price", title = "Property Price")
    )
    return chart.to_html()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Global Cost of Living"

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div(["Select cities to explore",
                dcc.Dropdown(
                    id='Cities', 
                    value=["Istanbul"],
                    options=[{'label': i, 'value': i} for i in cities],
                    multi=True,
                    style={'height': '10px'})]),
            html.Div(["OR select a region to explore",
                dcc.Dropdown(
                    id='Regions', 
                    value=["Africa"],
                    options=[{'label': i, 'value': i} for i in regions],
                    multi=True)]),
            html.Div(["Select monthly costs",
                dcc.Dropdown(
                    id='cost_subset', 
                    value=["all"],
                    options=[{'label': i, 'value': i} for i in price_subset],
                    multi=True)]),
            html.Div(["Expected monthly earnings ($USD)",
                dcc.Input(id="Expected_earnings", 
                    type="number", 
                    placeholder=0, 
                    style={'marginRight':'10px'})
                ])],width= 4),
        dbc.Col([html.Iframe( id = "comparison_plot",
            style={'border-width': '0', 'width': '100%', 'height': '500px'},
            srcDoc= plot1(["Istanbul"]))
        ], width="auto"),
        dbc.Col([html.Iframe( id = "monthly_surplus",
            style={'border-width': '0', 'width': '100%',  'height': '500px'},
            srcDoc= plot2(["Istanbul"]))
        ], width="auto") 
    ]),
    dbc.Row([
        dbc.Col([html.Iframe( id = "heat_map",
            style={'border-width': '0', 'width': '100%', 'height': '500px'},
            srcDoc= plot3(["Istanbul"]))
            ], 
            width={"size": "auto","offset": 4}),
        dbc.Col([html.Iframe( id = "property_price",
            style={'border-width': '0', 'width': '100%', 'height': '500px'},
            srcDoc= plot4(["Istanbul"]))
        ], width="auto") 
    ]),
], fluid=True)

@app.callback(   
    Output('comparison_plot', 'srcDoc'),
    Output('monthly_surplus', 'srcDoc'),
    Output('heat_map', 'srcDoc'),
    Output('property_price', 'srcDoc'),
    Input('Cities','value'))

def update_output(city_name):
    return plot1(city_name), plot2(city_name), plot3(city_name), plot4(city_name)

if __name__ == '__main__':
    app.run_server(debug=True)

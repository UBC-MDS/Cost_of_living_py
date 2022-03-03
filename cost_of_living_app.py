from dash import Dash, html, dcc, Input, Output, State
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc

data = pd.read_csv("data/processed_data.csv")
regions = sorted(data["region"].unique())
price_subset = {"Monthly Rent":"rent_for_one_person", 
                "Public Transport": "transportation_public",
                "Basic Groceries": "grocery_for_one_person", 
                "Entertainment":"entertainment", 
                "Fitness":"fitness", 
                "Utilities":"utility_bills",	
                "Shopping": "shopping",	
                "All":"all", 
                "Childcare":"childcare_for_one_child"}

fnameDict = {'City': sorted(data["city"].unique()), 'Region': sorted(data["region"].unique())}
names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

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

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server
app.title = "Global Cost of Living"

colors = {"menues": "#fdf6e3",
        "fonts": "black"}
font = {"menues": 17}

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Explore Global Cost Of Living",
        color="primary"), 
    dbc.Row([
        dbc.Col([
            html.Div(["Select by:"], style={'fontSize': 22}), 
            dcc.RadioItems(
                id='selection_type',
                options=[{'label': k, 'value': k} for k in names],
                value='City',
                inputStyle={"margin-left": "25px", 
                    "margin-right": "5px", 
                    "fontSize": font["menues"], 
                    "color": colors["fonts"] }
                ),
            html.Br(),
            dcc.Dropdown(id='selection', multi=True, value=['New York'],
                style = {"backgroundColor":colors["menues"], 
                    "fontSize": font["menues"], 
                    "color": colors["fonts"]}),
            html.Br(),
            html.Br(),
            html.Div(["Select monthly costs"], style={'fontSize': 22}),
            dcc.Dropdown(
                id='cost_subset', 
                value=["All"],
                options=[{'label': i, 'value': i} for i in list(price_subset.keys())],
                multi=True,
                style = {"backgroundColor":colors["menues"], 
                    "fontSize": font["menues"], 
                    "color": colors["fonts"]}),
            html.Br(),
            html.Br(),
            html.Div(["Expected monthly earnings ($USD)"],style={'fontSize': 22}),
            dcc.Input(id="Expected_earnings", 
                type="number", 
                placeholder=0, 
                style={'marginRight':'10px',
                    "backgroundColor":colors["menues"], 
                    "fontSize": font["menues"], 
                    "color": colors["fonts"]})
            ],width= 3),
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
            width={"size": "auto","offset": 3}),
        dbc.Col([html.Iframe( id = "property_price",
            style={'border-width': '0', 'width': '100%', 'height': '500px'},
            srcDoc= plot4(["Istanbul"]))
        ], width="auto") 
    ]),
], fluid=True)

@app.callback(
    Output('selection', 'options'),
    [Input('selection_type', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in fnameDict[name]]

@app.callback(   
    Output('comparison_plot', 'srcDoc'),
    Output('monthly_surplus', 'srcDoc'),
    Output('heat_map', 'srcDoc'),
    Output('property_price', 'srcDoc'),
    Input('selection','value'))

def update_output(selection):
    if selection[0] in regions:
        city_name = data.loc[data.region == selection[0], "city"]
    else:
        city_name = selection 
    return plot1(city_name), plot2(city_name), plot3(city_name), plot4(city_name)

if __name__ == '__main__':
    app.run_server(debug=True)

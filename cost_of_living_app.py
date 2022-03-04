from turtle import width
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
def plot1(city_name,cost_subset):
    """
    Compare the specefic cost of living between selected cities.

    param: city_name A list of selected cities
    param: cost_subset A string of selected specific cost type
    return: A bar chart showing living cost in selected cities 
    """
    subset = data.loc[data["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.Y(cost_subset, title = str.capitalize(cost_subset)+"(USD)"),
         alt.X("city", title = "City", sort = "y", axis=alt.Axis(labelAngle=-45)),
         alt.Color("city",legend=None),
         tooltip=[
            alt.Tooltip(cost_subset),
        ]
    ).properties(
        title='Cost of living comparison',
    
    )
    return chart.to_html()

## THIS IS THE MONTHLY SURPLUS PLOT
def plot2(city_name, Expected_earnings):
    """
    Calculate expected monthly savings in selected cities.

    param: city_name A list of selected cities
    param: Expected_earnings An integer of expected monthly earning
    return: A bar chart showing monthly savings in selected cities 
    """
    pd.options.mode.chained_assignment = None
    subset = data.loc[data["city"].isin(city_name),:]
    if Expected_earnings == None:
        Expected_earnings = 0
    subset["monthly_surplus"] = Expected_earnings - subset["all"]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.Y("monthly_surplus", title = "Monthly Saving(USD)"),
         alt.X("city", title = "City", sort = "-y", axis=alt.Axis(labelAngle=-45)),
         alt.Color("city",legend=None),
         tooltip=[
            alt.Tooltip('monthly_surplus'),
        ]
    ).properties(
        title='Monthly saving comparison',
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
    html.Div(html.H1('Global Cost of Living', style={'backgroundColor':'#2eced0', 'textAlign': 'center'})), 
    dbc.Row([
        dbc.Col([
            html.Div(["Select by:",
                dcc.RadioItems(
                    id='selection_type',
                    options=[{'label': k, 'value': k} for k in names],
                    value='City',
                    inputStyle={"margin-left": "25px", "margin-right": "5px", }
                    )]),
            html.Br(),
            dcc.Dropdown(id='selection', multi=True, value=['New York']),
            html.Br(),
            html.Br(),
            html.Div(["Select monthly costs",
                dcc.Dropdown(
                    id='cost_subset', 
                    value="all",
                    options=[{'label': i, 'value': price_subset[i]} for i in list(price_subset.keys())],
                    multi=False)]),
            html.Br(),
            html.Br(),
            html.Div(["Expected monthly earnings ($USD)",
                dcc.Input(id="Expected_earnings", 
                    type="number", 
                    placeholder=0,
                    value=0, 
                    style={'marginRight':'10px'})
                ])],width= 3),
        dbc.Col([html.Iframe( id = "comparison_plot",
            style={'border-width': '0', 'width': '100%', 'height': '500px'},
            srcDoc= plot1(["New York"],"all"))
            ], width="auto"),
        dbc.Col([html.Iframe( id = "monthly_surplus",
            style={'border-width': '0', 'width': '100%',  'height': '500px'},
            srcDoc= plot2(["New York"], 3000))
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
    Input('selection','value'),
    Input('cost_subset','value'),
    Input('Expected_earnings','value'))

def update_output(selection,cost_subset,Expected_earnings):
    if selection[0] in regions:
        city_name = data.loc[data.region == selection[0], "city"]
    else:
        city_name = selection 
    return plot1(city_name,cost_subset), plot2(city_name, Expected_earnings), plot3(city_name), plot4(city_name)

if __name__ == '__main__':
    app.run_server(debug=True)

from logging import PlaceHolder
from dash import Dash, html, dcc, Input, Output, State
from vega_datasets import data
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc

data_df = pd.read_csv("data/processed_data.csv")
regions = sorted(data_df["region"].unique())
price_subset = {"Total Monthly cost":"all",
                "Basic Groceries": "grocery_for_one_person",
                "Childcare":"childcare_for_one_child", 
                "Entertainment":"entertainment", 
                "Fitness":"fitness", 
                "Monthly Rent":"rent_for_one_person", 
                "Public Transport": "transportation_public",
                "Shopping": "shopping",
                "Utilities":"utility_bills"}

fnameDict = {'City': sorted(data_df["city"].unique()), 'Region': sorted(data_df["region"].unique())}
names = list(fnameDict.keys())
nestedOptions = fnameDict[names[0]]

## THIS IS THE COST COMPARISON PLOT
def plot1(city_name,cost_subset):
    """
    Compare the specific cost of living between selected cities.

    param: city_name, A list of selected cities
    param: cost_subset, A string of selected specific cost type
    return: A bar chart showing living cost in selected cities 
    """
    subset = data_df.loc[data_df["city"].isin(city_name),:].copy()
    subset.loc[:, "working"] = subset.loc[:,cost_subset].sum(axis=1)

    idx = [list(price_subset.values()).index(x) for x in cost_subset]
    cat = [list(price_subset.keys())[x] for x in idx]
    y_title = ' + '.join(cat)

    chart = alt.Chart(subset).mark_bar().encode(
         alt.Y("working", title = f"{y_title}(USD)"),
         alt.X("city", title = "Cities", sort = "y", axis=alt.Axis(labelAngle=-45)),
         alt.Color("city",legend=None),
         tooltip= cost_subset
    ).properties(
        width=700
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
    subset = data_df.loc[data_df["city"].isin(city_name),:]
    if Expected_earnings == None:
        Expected_earnings = 0
    subset["monthly_surplus"] = Expected_earnings - subset["all"]
    chart = alt.Chart(subset).mark_bar().encode(
         alt.Y("monthly_surplus", title = "Monthly Saving(USD)"),
         alt.X("city", title = "Cities", sort = "-y", axis=alt.Axis(labelAngle=-45)),
         alt.Color("city",legend=None),
         tooltip=[
            alt.Tooltip('monthly_surplus'),
        ]
    ).properties(
        width=260
    )
    return chart.to_html()


## THIS IS THE HEAT MAP PLOT
def plot3(city_name, cost_subset): 
    """
    Visualize the selected cities on world map and how the selected specific cost type varies.
    param: city_name A list of selected cities
    param: cost_subset, A string of selected specific cost type
    return: A choropleth map with point graph showing varying cost types in selected cities 
    """
    subset = data_df.loc[data_df["city"].isin(city_name),:].copy()
    subset.loc[:, "working"] = subset.loc[:,cost_subset].sum(axis=1)

    idx = [list(price_subset.values()).index(x) for x in cost_subset]
    cat = [list(price_subset.keys())[x] for x in idx]
    y_title = ' + '.join(cat)
    world_map = alt.topo_feature(data.world_110m.url, feature ='countries')  
    map_click = alt.selection_multi(fields=['city'])
    # bar_click = alt.selection_multi(fields=['city'])

    # background
    background = alt.Chart(world_map).mark_geoshape(
         stroke='black',
         fill='lightgray').encode(
        ).project(type='equirectangular'
        ).properties(
            width=650,
            height=350
        )
    # city positions on background
    points = alt.Chart(subset).mark_circle().encode(
            longitude='longitude:Q',
            latitude='latitude:Q',
            color='city:N',
            size=alt.Size("working", scale=alt.Scale(range=[0, 1000]),
                          legend=alt.Legend(title=f"Sum of Selected Costs (USD)")),
            # opacity=alt.condition(map_click, alt.value(0.8), alt.value(0.2)),
            tooltip=(cost_subset + ['city', 'country']),
            stroke=alt.value('white')).project(type='equirectangular'
            ).add_selection(map_click)
            # .transform_filter(bar_click)

    # bar2 = plot2(city_name, Expected_earnings)
    # .encode(
    #     opacity=alt.condition(bar_click, alt.value(0.8), alt.value(0.2)),
    #     stroke=alt.condition(bar_click, alt.value('black'), alt.value('#ffffff00')),
    #     color='region:N').add_selection(bar_click).transform_filter(map_click)

    chart =  (background + points)

    return chart.to_html()

## THIS IS THE PROPERTY PRICE PLOT
def plot4(city_name):
    """
    Compare property prices between selected cities.
    param: city_name A list of selected cities
    return: A bar chart showing property prices in selected cities 
    """

    subset = data_df.loc[data_df["city"].isin(city_name),:]
    chart = alt.Chart(subset).mark_bar().encode(
        alt.X("city", title = "Cities",  axis=alt.Axis(labelAngle=-45)),
         alt.Y("property_price", title = "Property price/m^2(USD)"),
         alt.Color("city",legend=None),
         tooltip=[
            alt.Tooltip("property_price"),
        ]
    ).properties(
        width=260
    )
    return chart.to_html()


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Global Cost of Living"

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#2eced0",
    "color": "black"
}

sidebar = html.Div(
    [html.H2('Where Can I Afford To Move To?', style={"justify": "center", "textAlign": "center"}),
    html.H6("Explore the cost of living for a single person in different cities around the world", 
        style={"justify": "center", "textAlign": "center"}),
    html.Br(),
    html.Br(),
    "Select by:",
    dcc.RadioItems(
        id='selection_type',
        options=[{'label': k, 'value': k} for k in names],
        value='Region',
        inputStyle={"margin-left": "25px", "margin-right": "5px", }
        ),
    html.Br(),
    dcc.Dropdown(id='selection', multi=True, value=['Canada'],
     placeholder = "Select the cities or region" ),
    html.Br(),
    html.Br(),
    html.Div(["Select monthly costs",
        dcc.Dropdown(
            id='cost_subset', 
            value=["all"],
            options=[{'label': i, 'value': price_subset[i]} for i in list(price_subset.keys())],
            multi=True)]),
    html.Br(),
    html.Br(),
    html.Div(["Expected monthly earnings ($USD)",
        dcc.Input(id="Expected_earnings", 
            type="number", 
            placeholder=2000,
            value=2000, 
            style={'marginRight':'10px'})
        ]),
    html.Br(),
    html.Br(),
    html.H6("The currency unit has been converted from Euro to USD and the current rate is 1 Euro = 1.14 USD", 
        style={"justify": "center", "textAlign": "center"})
    ], style=SIDEBAR_STYLE,)

comparison_plot = dbc.Card([dbc.CardHeader('Monthly Cost Comparison'),
                            dbc.CardBody(dcc.Loading(
                            children = html.Iframe(
                                id = "comparison_plot",
                                style={'border-width': '0', 'width': '100%', 'height': '500px'},
                                srcDoc= plot1(["New York"],["all"]))
                                ))
                            ], style={"height": "30rem"})

monthly_surplus = dbc.Card([dbc.CardHeader('How much can you save a month?'),
                            dbc.CardBody(dcc.Loading(
                            [html.Iframe(
                                id = "monthly_surplus",
                                style={'border-width': '0', 'width': '100%',  'height': '500px'},
                                srcDoc= plot2(["New York"], 3000)), 
                            ]))
                            ], style={"height": "30rem"})

heat_map =  dbc.Card([dbc.CardHeader('Map of living costs'),
                            dbc.CardBody(dcc.Loading(
                            children = html.Iframe(
                                id = "heat_map",
                                style={'border-width': '0', 'width': '100%', 'height': '500px'},
                                srcDoc= plot3(["Istanbul"],["all"]))
                                ))
                            ], style={"height": "30rem"})                          
property_price = dbc.Card([dbc.CardHeader('Average property price per square meter'),
                            dbc.CardBody(dcc.Loading(
                            children = html.Iframe(
                                id = "property_price",
                                style={'border-width': '0', 'width': '100%', 'height': '500px'},
                                srcDoc= plot4(["Istanbul"]))
                                ))
                            ], style={"height": "30rem"})     

footer = html.Footer([dcc.Markdown(
    f"*The raw data for this dashboard was sourced from this [Kaggle dataset](https://www.kaggle.com/joeypp/cost-of-living-numbeo-dataset). For more details about data processing and the dashboard please refer to the projects [GitHub page](https://github.com/UBC-MDS/Cost_of_living_py).*"
    )], 
    style={
        "textAlign": "center",
        "justify": "center",
        "margin-top": 0,
        "margin-bottom": 0,
        "font-size": "11px",}
)
  
data_description = dbc.Accordion([
            dbc.AccordionItem([
                html.P("The sum of all monthly costs excluding childcare."),
                ], title = "All"),   
            dbc.AccordionItem([
                    html.P("Grocery for one person includes average price of basic fruits, vegetables, diary and meat consumed by one person in a month."),
                ], title="Basic Groceries"),
            dbc.AccordionItem([
                html.P("Monthly price of private, full day preschool or kindergarden for 1 kid."),
                ], title="Childcare"), 
            dbc.AccordionItem([
                    html.P("Entertainment cost includes liquor, cigarettes,dining out and movie cost."),
                ], title="Entertainment"),    
            dbc.AccordionItem([
                    html.P("Fitness club monthly fee for 1 adult"),
                ], title="Fitness"),  
            dbc.AccordionItem([
                    html.P("Rent for one person considers the average of rent for a one-bedroom in city center and outside city center."),
                ], title="Monthly Rent"),
            dbc.AccordionItem([
                    html.P("Public transportation includes average monthly cost of taxi's and monthly bus passes."),
                ], title="Public Transport"),
            dbc.AccordionItem([
                html.P("Shopping includes buying jeans, summer dress, sports shoes, leather shoes once per month."),
                ], title="Shopping"), 
            dbc.AccordionItem([
                html.P("Utlities includes monthly bill for Electricity, Heating, Cooling, Water, Garbage, Prepaid Mobile Tariff Local and Internet"),
                ], title="Utilities")          
])

how_it_works = dbc.Accordion([
            dbc.AccordionItem([
                html.P("Firstly choose whether you want to compare between select cities or all ctites from a particular region."),
                ], title = "Select between City and Region Option"),   
            dbc.AccordionItem([
                    html.P("After that choose the cities or a region from the drop down menu."),
                ], title="Drop down menu for cities or region"),
            dbc.AccordionItem([
                html.P("Select a monthly cost you would like to compare the cities with, the next tab provides detailed breakdown of each monthly cost."),
                ], title="Drop down menu for monthly cost"), 
            dbc.AccordionItem([
                    html.P("Enter monthly earnings."),
                ], title="In order to see how much one can save in different cities, enter your expected monthly earnings.")        
])



content = dbc.Container([
    dbc.Col([dbc.Tabs([
        dbc.Tab([ 
            html.Br(),
            dbc.Row([comparison_plot]),
            html.Br(),
            dbc.Row([
                dbc.Col([monthly_surplus]),
                dbc.Col([property_price]) 
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col([heat_map]),
            ]),
            html.Br(),
            html.Br(),
            dbc.Col([footer])
            ], label = 'Cost of Living Comparison'),
        dbc.Tab([ 
            html.Br(),
            "Here are some basic steps to help you interact with our app!",
            html.Br(),
            html.Br(),
            how_it_works
        ], label = 'How it works'),
        dbc.Tab([ 
            html.Br(),
            "All the data represents the year 2020.",
            html.Br(),
            html.Br(),
            data_description
        ], label = 'Monthly Cost Details')
    ], id="tabs-graph")], width={"offset": 3})
])



app.layout = html.Div([sidebar, content])

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
        city_name = data_df.loc[data_df["region"].isin(selection), "city"]
    else:
        city_name = selection 
    return plot1(city_name,cost_subset), plot2(city_name, Expected_earnings), plot3(city_name, cost_subset), plot4(city_name)
    



if __name__ == '__main__':
    app.run_server(debug=True)

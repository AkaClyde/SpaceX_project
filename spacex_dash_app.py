# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn

spacex_df = pd.read_csv(r"C:\Users\34665\Desktop\Coursera\Visualitazion\bbdd_Dashboard_SpaceX.csv", index_col="Unnamed: 0")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[{'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True
                                ),
                                
                                #html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',  min=0, max=10000, step=1000,  marks={0: '0',2500: '2500', 5000: '5000', 7500:'7500', 10000:'10000'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total success launches')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_count = filtered_df[filtered_df['class'] == 1]['class'].count()
        failure_count = filtered_df[filtered_df['class'] == 0]['class'].count()
        fig = px.pie(names=['Success', 'Failure'], values=[success_count, failure_count], title="Success and Failure Landings for site " + entered_site)
        return fig
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# add callback decorator
#@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
#              Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value'))

#def get_scatter_chart(entered_site, payload_mass):
#    
#    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] < payload_mass]
#    if entered_site == 'ALL':  
#        fig = seaborn.scatterplot(data=filtered_df, x='Payload Mass (kg)', y='class', hue='Booster Version Category').set(title='Correlation between Payload Mass and Success for all sites')
#        return fig
#    else:
#        filtered2_df = filtered_df[filtered_df['Launch Site']== entered_site]
#        fig = seaborn.scatterplot(data=filtered2_df, x='Payload Mass (kg)', y='class', hue='Booster Version Category').set(title='Correlation between Payload Mass and Success for site: '+ entered_site)
#        return fig
        
# Run the app
if __name__ == '__main__':
    app.run_server()

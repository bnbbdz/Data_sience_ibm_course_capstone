# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Create dropdown list
LaunchSite_list = spacex_df['Launch Site'].unique().tolist()
LaunchSite_all = ['All Site'] + LaunchSite_list

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options= [
                                                {'label' : x , 'value' : x} for x in LaunchSite_all
                                                    ],
                                            value = 'All Site',
                                            placeholder = 'Select a Launch Site',
                                            searchable = True,
                                            style = {'textAlign' : 'center' , 'width' : '80%' , 'padding' : '3px' , 'font-size' : 20}
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0,
                                                max = 10000,
                                                step = 1000,
                                                marks = {   0 : '0 (kg)',
                                                            1000 : '1k (kg)',
                                                            2000 : '2k (kg)',
                                                            3000 : '3k (kg)',
                                                            4000 : '4k (kg)',
                                                            5000 : '5k (kg)',
                                                            6000 : '6k (kg)',
                                                            7000 : '7k (kg)',
                                                            8000 : '8k (kg)',
                                                            9000 : '9k (kg)',
                                                            10000 : '10k (kg)',
                                                        },
                                                value = [min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(  Output(component_id = 'success-pie-chart' , component_property = 'figure'),
                Input(component_id = 'site-dropdown' , component_property = 'value')
            )
#Create pie chart            
def create_pie (data):
    if data == 'All Site':
        spacex_df_pie = spacex_df[['Launch Site','class']].groupby(by = 'Launch Site').sum()
        spacex_df_pie.reset_index(inplace = True)
        pie_chart = px.pie(spacex_df_pie , values = 'class' , names = 'Launch Site' , title = 'The total success launches for all Sites')
        return pie_chart 
    else:
        spacex_df_filter  = spacex_df[spacex_df['Launch Site'] == data]
        spacex_df_pie = spacex_df_filter[['Launch Site','class']].groupby(by = 'class').count()
        spacex_df_pie.reset_index(inplace = True)
        pie_chart = px.pie(spacex_df_pie, values = 'Launch Site', names = 'class' , title = 'The total success or failed launches in Site {}'.format(data))
        return pie_chart      
                   

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(  Output(component_id = 'success-payload-scatter-chart' , component_property = 'figure'),
            [   Input(component_id = 'site-dropdown', component_property = 'value' ),
                Input(component_id = 'payload-slider', component_property = 'value')
            ]
            )
def create_scatter(data,payload):
    spacex_df_payload = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if data == 'All Site':
        scatter_chart = px.scatter(spacex_df_payload, x = 'Payload Mass (kg)' , y = 'class' , color="Booster Version Category" , title = 'Correlation between Payload and Success for all Sites')
        return scatter_chart 
    else:
        spacex_df_filter  = spacex_df_payload[spacex_df_payload['Launch Site'] == data]
        scatter_chart = px.scatter(spacex_df_filter, x = 'Payload Mass (kg)' , y = 'class' , color="Booster Version Category" , title = 'Correlation between Payload and Success in Site {}'.format(data))
        return scatter_chart   

# Run the app
if __name__ == '__main__':
    app.run_server()

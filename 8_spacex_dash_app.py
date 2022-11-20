

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Read the airline data into pandas dataframe
print(os.chdir('/Volumes/private/Hobbies/Coursera/Python/Applied Data Science Capstone/'))
spacex_df = pd.read_csv("8_spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


# Helper Variables 
launch_sites = spacex_df['Launch Site'].value_counts().index.to_list()
launch_sites.insert(0,'all')

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(launch_sites, 'all',id='site-dropdown'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                marks={0: '0', 2500: '2500',
                                5000: '5000',
                                7500: '7500',
                                10000: '10000'},
                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
     )

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    
    data = filtered_df
    if entered_site == 'all':
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Sucess of Launches by Launch Site ' )
        return fig
    else:
        data = filtered_df.query("`Launch Site` == @entered_site")
        fig = px.pie(data, names='class', color='class', 
        title='Total Success of Launches for Site' +entered_site,
        color_discrete_map={0:'red',
                            1:'green'
                            }
                            )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value'),


     )
        
def update_graph(entered_site,slider):
    filtered_df = spacex_df
    
    data = filtered_df
    data = data[data['Payload Mass (kg)'].between(slider[0],slider[1])]
    print(slider[0],slider[1])
    if entered_site == 'all':

        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig
    else:
        data = filtered_df.query("`Launch Site` == @entered_site")
        data = data[data['Payload Mass (kg)'].between(slider[0],slider[1])]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)

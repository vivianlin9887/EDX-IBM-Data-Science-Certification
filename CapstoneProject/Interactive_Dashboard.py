import dash
import html as html
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

spacex_df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}
                                        ),
                                # Task 1:
                                html.Div([dcc.Dropdown(id='site-dropdown',
                                                      options=[
                                                       {'label': 'All Sites', 'value': 'ALL'},
                                                       {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                       {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                       {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                       {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                                      value='ALL',
                                                      placeholder="Select a Launch Site here",
                                                      searchable=True
                                                        ),
                                          html.Div(dcc.Graph(id='success-pie-chart'))
                                          ]),
                                html.Br(),
                                # Task 3: Add Range Slider
                                html.Div([html.Label("Payload range (Kg):"),
                                          dcc.RangeSlider(id='payload-slider',
                                                          min=0, max=10000, step=1000,
                                                          marks={0: '0', 2500: '2500', 5000: '5000',
                                                                 7500: '7500', 10000: '1000'},
                                                          value=[0, 10000]),
                                          dcc.Graph(id='success-payload-scatter-chart')
                                          ]),
                                ])


# Task 2: Add callback function for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        # Omitting values will count the occurrence of each label
        fig = px.pie(filtered_df, names='class', title=f"Total Success Launches for site {entered_site}")
        return fig


# Task 4: Add callback function for scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, entered_payload):
    filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                            (spacex_df['Payload Mass (kg)'] >= entered_payload[0]) &
                            (spacex_df['Payload Mass (kg)'] <= entered_payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)'] >= entered_payload[0]) &
                                   (spacex_df['Payload Mass (kg)'] <= entered_payload[1])],
                         x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)

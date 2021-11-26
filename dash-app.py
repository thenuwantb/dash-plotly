import pandas as pd
import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

data = pd.read_csv('accident_merge_casuality.csv')
data_for_graph = data[['accident_index', 'date', 'light_conditions']]

# data type converstions
data_for_graph['date'] = pd.to_datetime(data_for_graph['date'])
data_for_graph['month'] = data_for_graph['date'].dt.strftime('%B')

# creating dash app
app = dash.Dash()

app.layout = html.Div([
    html.H1(children="Accidents at different light conditions - UK",
            ),

    dcc.Dropdown(
        id='light-condition-dropdown',
        options=[
            {'label': 'Day Light', 'value': 1},
            {'label': 'Darkness - lights lit', 'value': 4},
            {'label': 'Darkness - lights unlit', 'value': 5},
            {'label': 'Darkness - no lighting', 'value': 6},
            {'label': 'Darkness - lighting unknown', 'value': 7}
        ],
        value='1',
        style={'width': "50%"}
    ),

    html.Div([
        dcc.Graph(id='line-graph')
    ])

])


@app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='light-condition-dropdown', component_property='value')

)
def update_graph(light_condition):
    data_light_condition = data_for_graph[data_for_graph['light_conditions'] == light_condition]
    accident_month_light_condition = data_light_condition.groupby('month')['accident_index'].count().to_frame()

    accident_month_light_condition['month'] = accident_month_light_condition.index

    sort_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    accident_month_light_condition.index = pd.CategoricalIndex(accident_month_light_condition['month'],
                                                               categories=sort_order,
                                                               ordered=True)
    accident_month_light_condition = accident_month_light_condition.sort_index().reset_index(drop=True)

    fig = px.line(accident_month_light_condition, x='month', y='accident_index',
                  labels=dict(month='Month (2019)', accident_index='Accidents'))
    return fig


app.run_server(debug=False)

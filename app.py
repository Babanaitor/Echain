
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.figure_factory as ff
import dash
import dash_table
from flask import (Flask, has_request_context)
import plotly.express as px
import numpy as np
import os
import xlrd
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background': '#111111', 'text': '#7FDBFF'}

conn = urllib.request.urlopen("https://api.thingspeak.com/channels/959649/feeds.json?api_key=BBSDRD383CP6DE7B")

response = conn.read()
data = json.loads(response)

df = data["feeds"]
df = pd.DataFrame(df)
print(df)
# for i in range(df["created_at"].count()):
df["date"] = df["created_at"].str[0:10] + " " + df["created_at"].str[12:19]

for i in range(df["date"].count()):
    df.loc[i, "datetime"] = datetime.datetime.strptime(df.loc[i, "date"], '%Y-%m-%d %H:%M:%S')
print(df["datetime"])

print(df["date"])
print(type(df.loc[2, "datetime"]))


conn.close()



app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='E-Chain Web APP',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # html.Div(children='E-Chain Web APP', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),

    dcc.Graph(
        id='houses_consumption_graph',
        figure={
            'data': [
                {'x': df["datetime"], 'y': df["field1"], 'type': 'bar', 'name': 'house1'},
                {'x': df["datetime"], 'y': df["field2"], 'type': 'bar', 'name': 'house2'},
                {'x': df["datetime"], 'y': df["field3"], 'type': 'bar', 'name': 'house3'},
                {'x': df["datetime"], 'y': df["field4"], 'type': 'bar', 'name': 'house4'},
                {'x': df["datetime"], 'y': df["field5"], 'type': 'bar', 'name': 'house5'},
                {'x': df["datetime"], 'y': df["field6"], 'type': 'bar', 'name': 'house4'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server()

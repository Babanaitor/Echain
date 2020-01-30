import pandas as pd
import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from time import sleep
import urllib
import json
import datetime
from flask import request
import plotly.graph_objects as go

VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world'],
    ['house1', '123456'],
    ['house2', '123456']
]

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

external_stylesheets = ['assets/codepen.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# conn = urllib.request.urlopen("https://api.thingspeak.com/channels/959649/feeds.json?api_key=BBSDRD383CP6DE7B")
# response = conn.read()
# data = json.loads(response)
# conn.close()
# df = data["feeds"]
# df = pd.DataFrame(df)
# df["date"] = df["created_at"].str[0:10] + " " + df["created_at"].str[11:19]
# for i in range(df["date"].count()):
#     df.loc[i, "datetime"] = datetime.datetime.strptime(df.loc[i, "date"], '%Y-%m-%d %H:%M:%S')
# df.to_excel("output.xlsx")


def zerofy(list1):
    for i in range(len(list1)):
        if list1[i] < 0:
            list1[i] = 0
    return list1


df = pd.read_excel('output1.xlsx')

house1_net = df['field7'].sum() - df['field1'].sum()
house2_net = df['field8'].sum() - df['field2'].sum()
house3_net = df['field9'].sum() - df['field3'].sum()
house4_net = df['field10'].sum() - df['field4'].sum()
house5_net = -df['field5'].sum()
house6_net = -df['field6'].sum()

houses_list_net = [house1_net, house2_net, house3_net, house4_net, house5_net, house6_net]

new_houses_list_net = houses_list_net
money_owed = [0, 0, 0, 0, 0, 0]
total_positive_power = 0
number_of_neg_houses = 0
neighbor_bill = [0,0,0,0,0,0]
for i in range(len(houses_list_net)):
    if houses_list_net[i] >= 0:
        # print(i)
        # print(houses_list_net)
        money_owed[i] = houses_list_net[i] * 0.0001
        total_positive_power = total_positive_power + houses_list_net[i]
        new_houses_list_net[i] = 0
    else:
        money_owed[i] = 0

# print("YOYOYO", new_houses_list_net)
break1 = 6
dewa_power = 0
while break1 > 0:
    for i in range(len(new_houses_list_net)):
        if new_houses_list_net[i] < 0:
            number_of_neg_houses = number_of_neg_houses + 1

    power_delivered = total_positive_power / number_of_neg_houses

    for j in range(len(new_houses_list_net)):
        if new_houses_list_net[j] < 0:
            if power_delivered >= (-1)*new_houses_list_net[j]:
                neighbor_bill[j] = neighbor_bill[j] + new_houses_list_net[j]*(-0.0001)


                # print('loooook at meeeeeeeeee;,',new_houses_list_net[j], neighbor_bill[j],power_delivered)
            elif power_delivered < (-1)*new_houses_list_net[j]:
                neighbor_bill[j] = neighbor_bill[j]+power_delivered*(0.0001)
                print("if pd < house net ", neighbor_bill)

            new_houses_list_net[j] = new_houses_list_net[j] + power_delivered

    total_positive_power = 0
    for i in range(len(new_houses_list_net)):
        if all(t >= 0 for t in new_houses_list_net):
            dewa_power = sum(new_houses_list_net)
            break1 = 0
        if new_houses_list_net[i] > 0:
            total_positive_power = total_positive_power + new_houses_list_net[i]
            new_houses_list_net[i] = 0

    number_of_neg_houses = 0
    break1 = break1 - 1
# print('dewa power', dewa_power)

dewa_bill=[0,0,0,0,0,0]
for i in range(len(new_houses_list_net)):
    if new_houses_list_net[i] < 0:
        dewa_bill[i] = new_houses_list_net[i]*-0.0003
        new_houses_list_net[i] = 0

    else:
        dewa_bill[i] = 0


bill_df = pd.DataFrame()
for i in range(len(new_houses_list_net)):
    if money_owed[i] > 0:
        bill_df.loc[i, 'dewa'] = 0
        bill_df.loc[i, 'neighbor'] = 0

        bill_df.loc[i, 'credit'] = money_owed[i]
        bill_df.loc[i, 'bill'] = 0

    else:
        bill_df.loc[i, 'dewa'] = dewa_bill[i]/0.0003
        bill_df.loc[i, 'neighbor'] =neighbor_bill[i]/0.0001
        bill_df.loc[i, 'credit'] = 0
        bill_df.loc[i, 'bill'] = dewa_bill[i] + neighbor_bill[i]


df['power_from_dewa_house1'] = df['field1'] - df['field7']
df['power_to_dewa_house1'] = df['field7'] - df['field1']
df['power_from_dewa_house2'] = df['field2'] - df['field8']
df['power_to_dewa_house2'] = df['field8'] - df['field2']
df['power_from_dewa_house3'] = df['field3'] - df['field9']
df['power_to_dewa_house3'] = df['field9'] - df['field3']
df['power_from_dewa_house4'] = df['field4'] - df['field10']
df['power_to_dewa_house4'] = df['field10'] - df['field4']

df['power_from_dewa_house1'] = zerofy(df['power_from_dewa_house1'])
df['power_to_dewa_house1'] = zerofy(df['power_to_dewa_house1'])
df['power_from_dewa_house2'] = zerofy(df['power_from_dewa_house2'])
df['power_to_dewa_house2'] = zerofy(df['power_to_dewa_house2'])
df['power_from_dewa_house3'] = zerofy(df['power_from_dewa_house3'])
df['power_to_dewa_house3'] = zerofy(df['power_to_dewa_house3'])
df['power_from_dewa_house4'] = zerofy(df['power_from_dewa_house4'])
df['power_to_dewa_house4'] = zerofy(df['power_to_dewa_house4'])

house1_p_in = df['power_from_dewa_house1'].sum()
house1_p_out = df['power_to_dewa_house1'].sum()
house2_p_in = df['power_from_dewa_house2'].sum()
house2_p_out = df['power_to_dewa_house2'].sum()
house3_p_in = df['power_from_dewa_house3'].sum()
house3_p_out = df['power_to_dewa_house3'].sum()
house4_p_in = df['power_from_dewa_house4'].sum()
house4_p_out = df['power_to_dewa_house4'].sum()
house5_p_in = df['field5'].sum()
house6_p_in = df['field6'].sum()

labels = ['Private PV System', 'Neighbors', 'DEWA']

values_h1 = [df['field7'].sum()/df['field1'].sum(),bill_df.loc[0,'neighbor']/df['field1'].sum(), bill_df.loc[0, 'dewa']/df['field1'].sum()]
values_h2 = [df['field8'].sum()/df['field2'].sum(),bill_df.loc[1,'neighbor']/df['field1'].sum(), bill_df.loc[1, 'dewa']/df['field1'].sum()]
values_h3 = [df['field9'].sum()/df['field3'].sum(),bill_df.loc[2,'neighbor']/df['field1'].sum(), bill_df.loc[2, 'dewa']/df['field1'].sum()]
values_h4 = [df['field10'].sum()/df['field4'].sum(),bill_df.loc[3,'neighbor']/df['field1'].sum(), bill_df.loc[3, 'dewa']/df['field1'].sum()]
values_h5 = [0,bill_df.loc[4,'neighbor']/df['field1'].sum(), bill_df.loc[4, 'dewa']/df['field1'].sum()]
values_h6 = [0,bill_df.loc[5,'neighbor']/df['field1'].sum(), bill_df.loc[5, 'dewa']/df['field1'].sum()]

app.layout = html.Div(style={'backgroundColor': colors['background'], 'display': 'hidden'}, children=[

    html.H2(id='show-output', children=''),
    html.Button('Authenticate', id='button'),

])


@app.callback(
    Output(component_id='show-output', component_property='children'),
    [Input(component_id='button', component_property='n_clicks')]
)
def update_output_div(n_clicks):
    username = request.authorization['username']
    if n_clicks:
        return ""
    else:
        if username == "house1":
            app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

                html.H1(
                    children='E-Chain Web App',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.H2(
                    children='House 1',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),

                dcc.Graph(
                    id='house1_consumption_graph',

                    figure={
                        'data': [
                            {'x': df["datetime"], 'y': df["field1"], 'type': 'bar', 'name': 'house 1'},
                            {'x': df["datetime"], 'y': df["field7"], 'type': 'bar', 'name': 'panel house 1'},

                        ],
                        'layout': {
                            'title': "house 1 Consumption",
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            }
                        }
                    }
                ),

                # dcc.Graph(
                #     id='house1_production_graph',
                #     figure={
                #         'data': [
                #             {'x': df["datetime"], 'y': df["field7"], 'type': 'bar', 'name': 'panel house 1'},
                #         ],
                #         'layout': {
                #             'title': "house 1 Production",
                #             'plot_bgcolor': colors['background'],
                #             'paper_bgcolor': colors['background'],
                #             'font': {
                #                 'color': colors['text']
                #             }
                #         }
                #     }
                # ),

                # dcc.Graph(
                #     id='Microgrid_consumption',
                #     figure={
                #         'data': [
                #             {'x': df["datetime"], 'y': df["power_from_dewa_house1"], 'type': 'line',
                #              'name': 'extra power consumed from dewa'},
                #             {'x': df["datetime"], 'y': df["power_to_dewa_house1"], 'type': 'line',
                #              'name': 'extra power given to dewa'},
                #         ],
                #         'layout': {
                #             'title': "house 1 Microgrid power transfer",
                #             'plot_bgcolor': colors['background'],
                #             'paper_bgcolor': colors['background'],
                #             'font': {
                #                 'color': colors['text']
                #             }
                #         }
                #     }
                # ),
                dcc.Graph(
                    id='pi1',
                    figure={
                        'data': [go.Pie(labels=labels, values=values_h1)],

                        'layout': {
                            'title': "house 1 power consumption breakdown",
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {
                                'color': colors['text']
                            }
                        }
                    }
                ),
                html.H2(
                    children='Bill: ' + str(bill_df.loc[0, 'bill']) + ' AED',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
                html.H2(
                    children='Credit: ' + str(bill_df.loc[0, 'credit']) + ' AED',
                    style={
                        'textAlign': 'center',
                        'color': colors['text']
                    }
                ),
            ])

        return app.layout


app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server()

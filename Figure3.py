from turtle import fillcolor, title
from xxlimited import foo
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime
from datetime import timedelta

ng_data = pd.read_csv("NG_data_long.csv")
ng_data['Date']=pd.to_datetime(ng_data['Date'])
#print(ng_data.head())
ng_data.rename(columns={'Indicator Name':'Indicator',
                        'variable':'month',
                        'Date':'date',
                        'value':'cpi'},
                inplace=True)
#ng_data=ng_data.loc[ng_data['date']>pd.to_datetime('2014-01-01'),:]
ng_data=ng_data.loc[ng_data['date']>='2018-08-31',:]
ng_data=ng_data.loc[ng_data['date']<='2021-12-31',:]
food_df=ng_data.loc[ng_data["Indicator"]=="Food and non-alcoholic beverages, Percentage change, Previous year",:].copy()

#Set chart limits
x_min = food_df["date"].min() - timedelta(days=30)
x_max = food_df["date"].max() + timedelta(days=30)
y_min = food_df["cpi"].min() - 1
y_max = food_df["cpi"].max() + 1

key_dates = ['2018-08-31', '2019-08-31', '2020-12-31']
key_events = ['Before border closure',
                'After border closure',
                'After border reopening']
#color_list=['green','orange','firebrick']
color_list=['mediumseagreen','floralwhite','green']
#print(ng_data.info())

#Initialize an empty list of traces
data=[]

#Loop through the key_dates
for date_ in key_dates:
    #get the index of the active date
    date_idx = key_dates.index(date_)
    if date_idx<2:
        #Get the end date for the active period
        date_cutoff = key_dates[date_idx+1]
        #Extract the df for the active period
        date_df = food_df.loc[food_df["date"]<=date_cutoff,:]
        #Cut off the part of the food_df that has already been plotted
        food_df = food_df.loc[food_df["date"]>=date_cutoff]
    else:
        date_df=food_df
    date_df.sort_values('date',ascending=[True],inplace=True)
    #Create trace for the active period
    date_trace=go.Scatter(x=date_df["date"],
                            y=date_df["cpi"].round(1),
                            fill="tozeroy",
                            fillcolor=color_list[date_idx],
                            mode="lines+markers+text",
                            name=key_events[date_idx],
                            text=date_df["cpi"].round(1),
                            textposition="top center",
                            textfont_size=8,
                            hovertemplate=
                                    "Date: %{x} <br>" +
                                    "Food inflation (in %): %{y} <br>"
                                    "<extra></extra>",
                            line=dict(color="black")
                            )
    #Append trace to the list of traces
    data.append(date_trace)

before_closure = [{
                'x': 0.04, 'y': 0.25, 'xref': 'paper', 'yref': 'paper',
                'text': 'In the 12 months before border <br>' + 
                        'closure, food inflation hovered <br>' +
                        'around 13% year-on-year.',
                'font': {'size': 10, 'color': 'black'},
                #'bgcolor': 'rgb(237, 64, 200)',
                'showarrow': False
                }]

after_closure = [{
                'x': 0.55, 'y': 0.57, 'xref': 'paper', 'yref': 'paper',
                'text': 'Over the 17 months during which <br>' + 
                        'borders were closed, food inflation rose  <br>' + 
                        'in a steady but sustained manner,  <br>' +
                        'surpassing 19% in December 2020.',
                'font': {'size': 10, 'color': 'black'},
                'showarrow': False
                }]

after_reopening = [{
                    'x': 0.75, 'y': 0.95, 'xref': 'paper', 'yref': 'paper',
                    'text': 'Within 3 months after borders reopened, <br>' + 
                        'food inflation began to drop.',
                    'font': {'size': 10, 'color': 'black'},
                    'showarrow': False
                    }]

layout = go.Layout(title=dict(text="Figure 3: Border closure and food price index",
                                x=0.5,
                                y=0.92,
                                font_size=20),
                    xaxis=dict(range=[x_min, x_max],
                                minor_ticks="outside",
                                showgrid=False),
                    yaxis=dict(range=[y_min, y_max],
                                title='Food price index, % change, compared to previous year',
                                minor_ticks="outside",
                                showgrid=False),
                    annotations=before_closure,
                    showlegend=True,
                    legend=dict(y=1,x=0))

fig = go.Figure(data=data, layout=layout)

fig.data[1].visible=False
fig.data[2].visible=False

sliders = [
        {'steps': [
        {'method': 'update', 'label': 'Before border closure', 'args':[{'visible':[True, False, False]}, {"annotations":before_closure}]},
        {'method': 'update', 'label': 'After border closure', 'args':[{'visible':[True, True, False]}, {"annotations": after_closure}]},
        {'method': 'update', 'label': 'After border reopening', 'args':[{'visible':[True, True, True]}, {"annotations": after_reopening}]}
        ],
        'currentvalue':{"prefix": "Current data view: "},
        'pad':{"t": 50, "b":10, "l":300, "r":300},}]
fig.update_layout({"sliders": sliders})
#See more about sliders at: https://plotly.com/python/reference/layout/sliders/

pyo.plot(fig, filename="food_cpi.html")



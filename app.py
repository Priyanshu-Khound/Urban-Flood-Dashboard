
import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
from dateutil import parser
from datetime import *
from dateutil import parser
from dateutil.relativedelta import *
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import base64
from io import BytesIO
import geopandas as gp
import folium
import json

matplotlib.use('agg')

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(external_stylesheets=external_stylesheets)
server = app.server

df = df = pd.read_csv('data/cities.csv')



# app.layout = html.Div(id = 'parent', children = [
#     html.H1(id = 'H1', children = 'Urban Floods', style = {'textAlign':'center',\
#                                             'marginTop':40,'marginBottom':40}),

#         dcc.Dropdown( id = 'dropdown',
#         options = [
#             {'label':'Bengaluru', 'value':'Bengaluru' },
#             {'label': 'Hyderabad', 'value':'Hyderabad'},
#             {'label': 'Chennai', 'value':'Chennai'},
#             {'label': 'Mumbai', 'value':'Mumbai'},
#             {'label': 'Delhi', 'value':'Delhi'},
#             ],
#         value = 'Bengaluru'),
#         html.Div([
#         html.Div([dcc.Graph(id = 'bar_plot')],
#             className='box'),

#         html.Div([dcc.Graph(id = 'pie_plot')],
#             className="six columns"),
#         ]),
#         html.Div([
#             html.Div([dcc.Graph(id = 'damage')],className="six columns"),
#             html.Div(id = 'folium_map',className="six columns")
#         ])
#     ])

app.layout = html.Div([

    html.Div([
        #html.H1(children='URBAN FLOODS'),
        html.H1(html.Img(alt = "image", src=r'assets/Urban_Floods.gif', style={'width': '210px', 'height': '140px', 'border':'none', 'margin-top':'10px', 'radius':'10px'})),
        html.Label('Urban floods in India are a growing concern, fueled by rapid urbanization, poor drainage infrastructure, encroachment of water bodies, and erratic rainfall patterns. Cities across the country, including Bengaluru, Hyderabad, Chennai, Mumbai, and Delhi, regularly face inundation during monsoon seasons, leading to disruptions in daily life, damage to property, and loss of lives. The impact of urban floods extends beyond immediate physical damage, affecting public health, transportation systems, and the economy. Effective urban planning, sustainable drainage solutions, and disaster preparedness measures are crucial for mitigating the impact of urban floods and enhancing resilience in Indian cities.', 
                    style={'color':'rgb(33 36 35)', 'text-align':'justify', 'font-size':'10px', 'margin-top':'5px'}),
        # html.Br(),
        html.Img(alt = "image", src=r'assets/Delhi.png', style={'width': '250px', 'height': '250px', 'border':'none', 'margin-left':'1px'}) 
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Label("Choose the City:", style={'font-size': '40px'}), 
                html.Br(),
                dcc.Dropdown( id = 'dropdown',
            options = [
                {'label':'Bengaluru', 'value':'Bengaluru' },
                {'label': 'Hyderabad', 'value':'Hyderabad'},
                {'label': 'Chennai', 'value':'Chennai'},
                {'label': 'Mumbai', 'value':'Mumbai'},
                {'label': 'Delhi', 'value':'Delhi'},
                ],
            value = 'Bengaluru', style= {'margin-left': '1px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a', 'font-size': '20px'}),
            ], className='box', style={'margin-left': '280px'}),

            html.Div([
                html.Div([
                html.Div([
                    html.Label("Number of Flooding Events", style={'font-size': '20px'}),
                    # html.Br(), 
                    html.Br(), 
                    dcc.Graph(id = 'bar_plot')
                ], className='box', style={'width': '50%'}), 
                html.Div([
                    html.Label("Severity of the Events", style={'font-size': '20px'}),
                    # html.Br(), 
                    html.Br(), 
                    dcc.Graph(id = 'pie_plot')
                ], className='box', style={'width': '50%'}), 
            ], className='row'),

                

            html.Div([
                html.Div([
                    html.Label("Reported Damages (in Crore)", style={'font-size': '20px'}),
                    # html.Br(),
                    html.Br(), 
                    dcc.Graph(id = 'damage')
                ], className='box', style={'width': '50%'}), 
                html.Div([
                    html.Label("Affected Areas", style={'font-size': '20px'}),
                    # html.Br(),
                    html.Br(), 
                    html.Div(id = 'folium_map')
                ], className='box', style={'width': '50%'}), 
            ], className='row'),
        ], className='main'),
    ]),
])
])  


    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def graph_update(dropdown_value):
    print(dropdown_value)

    if dropdown_value == 'Bengaluru':
        b_df = df[df['city']=='bangalore']

        b_df = b_df[b_df['category'].notna()]
        b_df = b_df[b_df['category'].str.contains('flood|Flood')]

        b_df = b_df[b_df['location'].notna()]
        b_df = b_df[b_df['location'].str.contains('Bengaluru|Bangalore|Karnataka')]

        b_df = b_df.reset_index(inplace=False)

        month_year = []

        for i in range(len(b_df['publish date'])):
            if "present" in b_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(b_df['publish date'][i])
            except:
                NOW = datetime.now()
                if 'month' in b_df['publish date'][i].lower():
                    datee = NOW-relativedelta(months=int(b_df['publish date'][i].lower().split(' ')[0]))
                elif 'week' in b_df['publish date'][i].lower():
                    NOW-relativedelta(weeks=int(b_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))
            #print(datee.year)
            #print()

        b_df['month_year'] = month_year

        key = []
        values = []
        for i in b_df['month_year'].unique():
            try:
                if i.split('-')[1] in key:
                    v = key.index(i.split('-')[1])
                    values[v] = values[v]+1
                    continue
                key.append(i.split('-')[1])
                values.append(1)
            except:
                continue
        
        fig = go.Figure([go.Bar(x = key, y = values,\
                         marker_color = 'firebrick')
                         ])
        
        fig.update_layout(#title = 'Frequency of Flood Events',
                          xaxis_title = 'Year',
                          yaxis_title = 'Frequency'
                          )

    if dropdown_value == 'Hyderabad':
        b_df = df[df['city']=='hyderabad']

        b_df = b_df[b_df['category'].notna()]
        b_df = b_df[b_df['category'].str.contains('flood|Flood')]

        b_df = b_df[b_df['location'].notna()]
        b_df = b_df[b_df['location'].str.contains('Hyderabad|Telangana')]
        b_df = b_df.reset_index(inplace=False)

        month_year = []

        for i in range(len(b_df['publish date'])):
            if "present" in b_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(b_df['publish date'][i])
            except:
                    NOW = datetime(2024,1,1)
                    if 'month' in b_df['publish date'][i].lower():
                        datee = NOW-relativedelta(months=int(b_df['publish date'][i].lower().split(' ')[0]))
                    elif 'week' in b_df['publish date'][i].lower():
                        NOW-relativedelta(weeks=int(b_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        b_df['month_year'] = month_year

        key = []
        values = []
        for i in b_df['month_year'].unique():
            try:
                if i.split('-')[1] in key:
                    v = key.index(i.split('-')[1])
                    values[v] = values[v]+1
                    continue
                key.append(i.split('-')[1])
                values.append(1)
            except:
                continue
        
        fig = go.Figure([go.Bar(x = key, y = values,\
                         marker_color = 'firebrick')
                         ])
        
        fig.update_layout(#title = 'Frequency of Flood Events',
                          xaxis_title = 'Year',
                          yaxis_title = 'Frequency'
                          )

    if dropdown_value == 'Chennai':
        b_df = df[df['city']=='chennai']

        b_df = b_df[b_df['category'].notna()]
        b_df = b_df[b_df['category'].str.contains('flood|Flood')]

        b_df = b_df[b_df['location'].notna()]
        b_df = b_df[b_df['location'].str.contains('Chennai|chennai|Tamil Nadu')]
        b_df = b_df.reset_index(inplace=False)

        month_year = []
        year = []

        for i in range(len(b_df['publish date'])):
            if "present" in b_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(b_df['publish date'][i])
            except:
                try:
                    datee = parser.parse(b_df['start_date'][i])
                except:
                    NOW = datetime.now()
                    if 'month' in b_df['publish date'][i].lower():
                        datee = NOW-relativedelta(months=int(b_df['publish date'][i].lower().split(' ')[0]))
                    elif 'week' in b_df['publish date'][i].lower():
                        NOW-relativedelta(weeks=int(b_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))
            year.append(datee.year)

        b_df['month_year'] = month_year
        

        key = []
        values = []
        for i in b_df['month_year'].unique():
            try:
                if i.split('-')[1] in key:
                    v = key.index(i.split('-')[1])
                    values[v] = values[v]+1
                    continue
                key.append(i.split('-')[1])
                values.append(1)
            except:
                continue
        d = pd.DataFrame()
        d['key'] = key
        d['values'] = values
        d = d.sort_values(by='key')
        fig = go.Figure([go.Bar(x = d['key'], y = d['values'],\
                         marker_color = 'firebrick')
                         ])
        
        fig.update_layout(#title = 'Frequency of Flood Events',
                          xaxis_title = 'Year',
                          yaxis_title = 'Frequency',
                          xaxis=dict(autorange="reversed")
                          )

    
    if dropdown_value == 'Mumbai':
        b_df = df[df['city']=='mumbai']

        b_df = b_df[b_df['category'].notna()]
        b_df = b_df[b_df['category'].str.contains('flood|Flood')]

        b_df = b_df[b_df['location'].notna()]
        b_df = b_df[b_df['location'].str.contains('Mumbai|mumbai|Maharashtra')]
        b_df = b_df.reset_index(inplace=False)

        month_year = []

        for i in range(len(b_df['publish date'])):
            if "present" in b_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(b_df['publish date'][i])
            except:
                try:
                    datee = parser.parse(b_df['start_date'][i])
                except:
                    NOW = datetime.now()
                    if 'month' in b_df['publish date'][i].lower():
                        datee = NOW-relativedelta(months=int(b_df['publish date'][i].lower().split(' ')[0]))
                    elif 'week' in b_df['publish date'][i].lower():
                        NOW-relativedelta(weeks=int(b_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        b_df['month_year'] = month_year

        key = []
        values = []
        for i in b_df['month_year'].unique():
            try:
                if i.split('-')[1] in key:
                    v = key.index(i.split('-')[1])
                    values[v] = values[v]+1
                    continue
                key.append(i.split('-')[1])
                values.append(1)
            except:
                continue
        
        fig = go.Figure([go.Bar(x = key, y = values,\
                         marker_color = 'firebrick')
                         ])
        
        fig.update_layout(#title = 'Frequency of Flood Events',
                          xaxis_title = 'Year',
                          yaxis_title = 'Frequency'
                          ) 

    if dropdown_value == 'Delhi':
        b_df = df[df['city']=='delhi']

        b_df = b_df[b_df['category'].notna()]
        b_df = b_df[b_df['category'].str.contains('flood|Flood')]

        b_df = b_df[b_df['location'].notna()]
        b_df = b_df[b_df['location'].str.contains('Delhi|delhi')]
        b_df = b_df.reset_index(inplace=False)

        month_year = []

        for i in range(len(b_df['publish date'])):
            if "present" in b_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(b_df['publish date'][i])
            except:
                try:
                    datee = parser.parse(b_df['start_date'][i])
                except:
                    NOW = datetime.now()
                    if 'month' in b_df['publish date'][i].lower():
                        datee = NOW-relativedelta(months=int(b_df['publish date'][i].lower().split(' ')[0]))
                    elif 'week' in b_df['publish date'][i].lower():
                        NOW-relativedelta(weeks=int(b_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        b_df['month_year'] = month_year

        key = []
        values = []
        for i in b_df['month_year'].unique():
            try:
                if i.split('-')[1] in key:
                    v = key.index(i.split('-')[1])
                    values[v] = values[v]+1
                    continue
                key.append(i.split('-')[1])
                values.append(1)
            except:
                continue
        
        fig = go.Figure([go.Bar(x = key, y = values,\
                         marker_color = 'firebrick')
                         ])
        
        fig.update_layout(#title = 'Frequency of Flood Events',
                          xaxis_title = 'Year',
                          yaxis_title = 'Frequency'
                          ) 
    return fig  

@app.callback(Output(component_id='pie_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def pie_update(dropdown_value):
    print(dropdown_value)

    if dropdown_value == 'Bengaluru':
        sever_df = pd.read_csv('data/sever_df_bengaluru.csv')

        key = []
        value = []
        hue = []
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts():
            value.append(i)
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts().index:
            key.append(i[0])
            hue.append(i[1])

        fig = make_subplots(rows=2,
        cols=5, specs = [[{'type':'domain'}] * 5] * 2,
        subplot_titles=sever_df['year'].unique().tolist())

        col = sever_df['year'].unique()
        y = 0

        
        for i in range(1,3):
            for j in range(1,6):
                fig.add_trace(
                    go.Pie(labels=sever_df[sever_df['year']==col[y]]['classification'].value_counts().index,
                        values=sever_df[sever_df['year']==col[y]]['classification'].value_counts(),
                        domain=dict(x=[0, 0.5]),),
                    row=i,
                    col=j)
                y+=1
    
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ))

    if dropdown_value == 'Hyderabad':
        sever_df = pd.read_csv('data/sever_df_hyderabad.csv')

        key = []
        value = []
        hue = []
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts():
            value.append(i)
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts().index:
            key.append(i[0])
            hue.append(i[1])

        fig = make_subplots(rows=2,
        cols=5, specs = [[{'type':'domain'}] * 5] * 2,
        subplot_titles=sever_df['year'].unique().tolist())

        col = sever_df['year'].unique()
        y = 0

        
        for i in range(1,3):
            for j in range(1,6):
                try:
                    fig.add_trace(
                        go.Pie(labels=sever_df[sever_df['year']==col[y]]['classification'].value_counts().index,
                            values=sever_df[sever_df['year']==col[y]]['classification'].value_counts(),
                            domain=dict(x=[0, 0.5]),),
                        row=i,
                        col=j)
                except:
                    break
                y+=1
    
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ))

    if dropdown_value == 'Chennai':
        sever_df = pd.read_csv('data/sever_df_chennai.csv')

        key = []
        value = []
        hue = []
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts():
            value.append(i)
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts().index:
            key.append(i[0])
            hue.append(i[1])

        fig = make_subplots(rows=2,
        cols=5, specs = [[{'type':'domain'}] * 5] * 2,
        subplot_titles=sever_df['year'].unique().tolist())

        col = sever_df['year'].unique()
        y = 0

        
        for i in range(1,3):
            for j in range(1,6):
                fig.add_trace(
                    go.Pie(labels=sever_df[sever_df['year']==col[y]]['classification'].value_counts().index,
                        values=sever_df[sever_df['year']==col[y]]['classification'].value_counts(),
                        domain=dict(x=[0, 0.5]),),
                    row=i,
                    col=j)
                y+=1
    
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ))
        
    if dropdown_value == 'Mumbai':
        sever_df = pd.read_csv('data/sever_df_mumbai.csv')

        key = []
        value = []
        hue = []
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts():
            value.append(i)
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts().index:
            key.append(i[0])
            hue.append(i[1])

        fig = make_subplots(rows=2,
        cols=5, specs = [[{'type':'domain'}] * 5] * 2,
        subplot_titles=sever_df['year'].unique().tolist())

        col = sever_df['year'].unique()
        y = 0

        
        for i in range(1,3):
            for j in range(1,6):
                fig.add_trace(
                    go.Pie(labels=sever_df[sever_df['year']==col[y]]['classification'].value_counts().index,
                        values=sever_df[sever_df['year']==col[y]]['classification'].value_counts(),
                        domain=dict(x=[0, 0.5]),),
                    row=i,
                    col=j)
                y+=1
    
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ))

    if dropdown_value == 'Delhi':
        sever_df = pd.read_csv('data/sever_df_delhi.csv')

        key = []
        value = []
        hue = []
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts():
            value.append(i)
        for i in sever_df['classification'].groupby([sever_df['year']]).value_counts().index:
            key.append(i[0])
            hue.append(i[1])

        fig = make_subplots(rows=2,
        cols=5, specs = [[{'type':'domain'}] * 5] * 2,
        subplot_titles=sever_df['year'].unique().tolist())

        col = sever_df['year'].unique()
        y = 0

        
        for i in range(1,3):
            for j in range(1,6):
                try:
                    fig.add_trace(
                        go.Pie(labels=sever_df[sever_df['year']==col[y]]['classification'].value_counts().index,
                            values=sever_df[sever_df['year']==col[y]]['classification'].value_counts(),
                            domain=dict(x=[0, 0.5]),),
                        row=i,
                        col=j)
                except:
                    break
                y+=1
    
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ))
    return fig  


@app.callback(Output(component_id='damage', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])
def damage_line(dropdown_value):
    print(dropdown_value)

    if dropdown_value == 'Bengaluru':

        gb_df = pd.read_csv('data/bangalore_with_severity.csv')

        gb_df = gb_df[gb_df['city']=='bangalore']

        gb_df = gb_df[gb_df['category'].notna()]
        gb_df = gb_df[gb_df['category'].str.contains('flood|Flood')]

        gb_df = gb_df[gb_df['location'].notna()]
        gb_df = gb_df[gb_df['location'].str.contains('Bengaluru|Bangalore|Karnataka')]

        gb_df = gb_df.reset_index()

        month_year = []

        for i in range(len(gb_df['publish date'])):
            if "present" in gb_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(gb_df['publish date'][i])
            except:
                datee = parser.parse(gb_df['publish date'][i])
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))
            #print(datee.year)
            #print()

        gb_df['month_year'] = month_year
                
        month = []
        damages = []
        site = []
        traces=[]
        
        for i in range(gb_df.shape[0]):
            try:
                if 'crore' in gb_df['damage'][i] or 'INR' in gb_df['damage'][i] or 'Rs' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
                    te = gb_df['damage'][i].replace('[','').replace(']','')
                    for k in te.split('Rs'):
                        if 'crore' in k:
                            num = k.split('crore')[0].strip(".|'").strip().replace(',','')
                            n = re.findall(r'\d+', num)
                            damages.append(int(n[0]))
                            u = gb_df['url'][i].split('/')[2]
                            if 'www.' in u:
                                u = u.split('.')[1]
                            else:
                                u = u.split('.')[0]
                            site.append(u)
                            month.append(datetime.strptime(gb_df['month_year'][i].split('-')[1], "%Y").year)
                            break
            #     elif 'million' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'million' in k:
            #                 print('$ ',k.split('million')[0].strip(".|'").strip(), ' million')
            #                 break
            #     elif 'billion' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'billion' in k:
            #                 print('$ ',k.split('billion')[0].strip(".|'").strip(' '), ' billion')
            #                 break
            
            except:
                continue

        dam_df = pd.DataFrame({'month':month, 'damages':damages, 'site':site})
        dam_df = dam_df.sort_values(by='month',ascending=False).reset_index(drop=True)
        dam_df = dam_df[dam_df['damages']<3000]
        avg = dam_df.groupby(dam_df['month'])['damages'].transform('mean')

        print(dam_df["month"].tolist())
        #p = sns.scatterplot(data = dam_df, x='month', y='damages', hue='site')
        #sns.lineplot(x = dam_df['month'],y = avg, color='black', alpha=0.3, label='Average')
        #plt.legend(loc='right', bbox_to_anchor=(1.5, 0.5), fontsize='8')
        #plt.xlabel('Month-Year')
        #plt.ylabel('Damages (in Crore)')
        #plt.xticks(rotation=90)
        
        #fig = go.Figure([go.Scatter(x = dam_df['month'], y = dam_df['damages'], mode = 'markers', marker_color = dam_df['site'], \
        #                 line = dict(color = 'firebrick', width = 4))
        #                 ])

        #for x, d in dam_df.groupby('site'):

         #   traces.append(go.Scatter(x=dam_df.month, y=dam_df.damages, name=x))

        #fig = go.Figure(data=traces)
        
        #fig.update_layout(title = 'Estimated Damages',
         #                 xaxis_title = 'Year',
          #                yaxis_title = 'Estimated Damages (in Crore)'
           #               )
           
        fig = px.scatter(dam_df, x="month", y="damages", color="site")
        #fig = go.Figure([go.Scatter(x=dam_df['month'], y=dam_df['damages'], fill=dam_df['site'])])
        fig.add_traces(go.Scatter(x=dam_df['month'], y=avg, mode='lines', name='average'))
        
        
        #fig = px.line(x=month, y=damages, color=site)
        fig.update_layout(
            xaxis=dict(
            type='date',
            title='year'
            )
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        
    elif dropdown_value == 'Hyderabad':

        gb_df = pd.read_csv('data/hyderabad_with_severity.csv')
        gb_df = gb_df[gb_df['category'].notna()]
        gb_df = gb_df[gb_df['category'].str.contains('flood|Flood')]
        gb_df = gb_df[gb_df['location'].notna()]
        gb_df = gb_df[gb_df['location'].str.contains('Hyderabad|Telangana')]
        gb_df = gb_df.reset_index()

        month_year = []

        for i in range(len(gb_df['publish date'])):
            if "present" in gb_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(gb_df['publish date'][i])
            except:
                NOW = datetime.now()
                if 'month' in gb_df['publish date'][i].lower():
                    datee = NOW-relativedelta(months=int(gb_df['publish date'][i].lower().split(' ')[0]))
                elif 'week' in gb_df['publish date'][i].lower():
                    NOW-relativedelta(weeks=int(gb_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        gb_df['month_year'] = month_year
                
        month = []
        damages = []
        site = []
        traces=[]
        
        for i in range(gb_df.shape[0]):
            try:
                if 'crore' in gb_df['damage'][i] or 'INR' in gb_df['damage'][i] or 'Rs' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
                    te = gb_df['damage'][i].replace('[','').replace(']','')
                    for k in te.split('Rs'):
                        if 'crore' in k:
                            num = k.split('crore')[0].strip(".|'").strip().replace(',','')
                            n = re.findall(r'\d+', num)
                            damages.append(int(n[0]))
                            u = gb_df['url'][i].split('/')[2]
                            if 'www.' in u:
                                u = u.split('.')[1]
                            else:
                                u = u.split('.')[0]
                            site.append(u)
                            month.append(datetime.strptime(gb_df['month_year'][i].split('-')[1], "%Y").year)
                            break
            #     elif 'million' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'million' in k:
            #                 print('$ ',k.split('million')[0].strip(".|'").strip(), ' million')
            #                 break
            #     elif 'billion' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'billion' in k:
            #                 print('$ ',k.split('billion')[0].strip(".|'").strip(' '), ' billion')
            #                 break
            
            except:
                continue

        dam_df = pd.DataFrame({'month':month, 'damages':damages, 'site':site})
        dam_df = dam_df.sort_values(by='month',ascending=False).reset_index(drop=True)
        dam_df = dam_df[dam_df['damages']<3000]
        avg = dam_df.groupby(dam_df['month'])['damages'].transform('mean')

        print(dam_df["month"].tolist())
        #p = sns.scatterplot(data = dam_df, x='month', y='damages', hue='site')
        #sns.lineplot(x = dam_df['month'],y = avg, color='black', alpha=0.3, label='Average')
        #plt.legend(loc='right', bbox_to_anchor=(1.5, 0.5), fontsize='8')
        #plt.xlabel('Month-Year')
        #plt.ylabel('Damages (in Crore)')
        #plt.xticks(rotation=90)
        
        #fig = go.Figure([go.Scatter(x = dam_df['month'], y = dam_df['damages'], mode = 'markers', marker_color = dam_df['site'], \
        #                 line = dict(color = 'firebrick', width = 4))
        #                 ])

        #for x, d in dam_df.groupby('site'):

         #   traces.append(go.Scatter(x=dam_df.month, y=dam_df.damages, name=x))

        #fig = go.Figure(data=traces)
        
        #fig.update_layout(title = 'Estimated Damages',
         #                 xaxis_title = 'Year',
          #                yaxis_title = 'Estimated Damages (in Crore)'
           #               )
           
        fig = px.scatter(dam_df, x="month", y="damages", color="site")
        #fig = go.Figure([go.Scatter(x=dam_df['month'], y=dam_df['damages'], fill=dam_df['site'])])
        fig.add_traces(go.Scatter(x=dam_df['month'], y=avg, mode='lines', name='average'))
        
        
        #fig = px.line(x=month, y=damages, color=site)
        fig.update_layout(
            xaxis=dict(
            type='date',
            title='year'
            )
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    
    elif dropdown_value == 'Chennai':

        gb_df = pd.read_csv('data/chennai_with_severity.csv')

        gb_df = gb_df[gb_df['category'].notna()]
        gb_df = gb_df[gb_df['category'].str.contains('flood|Flood')]

        gb_df = gb_df[gb_df['location'].notna()]
        gb_df = gb_df[gb_df['location'].str.contains('Chennai|Tamil Nadu')]

        gb_df = gb_df.reset_index()

        month_year = []

        for i in range(len(gb_df['publish date'])):
            if "present" in gb_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(gb_df['publish date'][i])
                
            except:
                    NOW = datetime(2024,1,1)
                    if 'month' in gb_df['publish date'][i].lower():
                        datee = NOW-relativedelta(months=int(gb_df['publish date'][i].lower().split(' ')[0]))
                    elif 'week' in gb_df['publish date'][i].lower():
                        datee = NOW-relativedelta(weeks=int(gb_df['publish date'][i].lower().split(' ')[0]))
                    
            month_year.append(str(datee.month) + '-' + str(datee.year))
            #print(datee)
            
            # print(datee.year)
            

        gb_df['month_year'] = month_year
                
        month = []
        damages = []
        site = []
        traces=[]
        
        for i in range(gb_df.shape[0]):
            try:
                if 'crore' in gb_df['damage'][i] or 'INR' in gb_df['damage'][i] or 'Rs' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
                    te = gb_df['damage'][i].replace('[','').replace(']','')
                    for k in te.split('Rs'):
                        if 'crore' in k:
                            num = k.split('crore')[0].strip(".|'").strip().replace(',','')
                            n = re.findall(r'\d+', num)
                            damages.append(int(n[0]))
                            u = gb_df['url'][i].split('/')[2]
                            if 'www.' in u:
                                u = u.split('.')[1]
                            else:
                                u = u.split('.')[0]
                            site.append(u)
                            month.append(datetime.strptime(gb_df['month_year'][i].split('-')[1], "%Y").year)
                            break
            #     elif 'million' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'million' in k:
            #                 print('$ ',k.split('million')[0].strip(".|'").strip(), ' million')
            #                 break
            #     elif 'billion' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'billion' in k:
            #                 print('$ ',k.split('billion')[0].strip(".|'").strip(' '), ' billion')
            #                 break
            
            except:
                continue

        dam_df = pd.DataFrame({'month':month, 'damages':damages, 'site':site})
        dam_df = dam_df.sort_values(by='month',ascending=False).reset_index(drop=True)
        dam_df = dam_df[dam_df['damages']<20000]
        avg = dam_df.groupby(dam_df['month'])['damages'].transform('mean')

        print(dam_df["month"].tolist())
        #p = sns.scatterplot(data = dam_df, x='month', y='damages', hue='site')
        #sns.lineplot(x = dam_df['month'],y = avg, color='black', alpha=0.3, label='Average')
        #plt.legend(loc='right', bbox_to_anchor=(1.5, 0.5), fontsize='8')
        #plt.xlabel('Month-Year')
        #plt.ylabel('Damages (in Crore)')
        #plt.xticks(rotation=90)
        
        #fig = go.Figure([go.Scatter(x = dam_df['month'], y = dam_df['damages'], mode = 'markers', marker_color = dam_df['site'], \
        #                 line = dict(color = 'firebrick', width = 4))
        #                 ])

        #for x, d in dam_df.groupby('site'):

         #   traces.append(go.Scatter(x=dam_df.month, y=dam_df.damages, name=x))

        #fig = go.Figure(data=traces)
        
        #fig.update_layout(title = 'Estimated Damages',
         #                 xaxis_title = 'Year',
          #                yaxis_title = 'Estimated Damages (in Crore)'
           #               )
           
        fig = px.scatter(dam_df, x="month", y="damages", color="site")
        #fig = go.Figure([go.Scatter(x=dam_df['month'], y=dam_df['damages'], fill=dam_df['site'])])
        fig.add_traces(go.Scatter(x=dam_df['month'], y=avg, mode='lines', name='average'))
        
        
        #fig = px.line(x=month, y=damages, color=site)
        fig.update_layout(
            xaxis=dict(
            type='date',
            title='year'
            )
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    elif dropdown_value == 'Mumbai':

        gb_df = pd.read_csv('data/mumbai_with_severity.csv')

        gb_df = gb_df[gb_df['category'].notna()]
        gb_df = gb_df[gb_df['category'].str.contains('flood|Flood')]

        gb_df = gb_df[gb_df['location'].notna()]
        gb_df = gb_df[gb_df['location'].str.contains('Mumbai|Maharashtra')]

        gb_df = gb_df.reset_index()


        month_year = []

        for i in range(len(gb_df['publish date'])):
            if "present" in gb_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(gb_df['publish date'][i])
            except:
                NOW = datetime.now()
                if 'month' in gb_df['publish date'][i].lower():
                    datee = NOW-relativedelta(months=int(gb_df['publish date'][i].lower().split(' ')[0]))
                elif 'week' in gb_df['publish date'][i].lower():
                    NOW-relativedelta(weeks=int(gb_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        gb_df['month_year'] = month_year
                
        month = []
        damages = []
        site = []
        traces=[]
        
        for i in range(gb_df.shape[0]):
            try:
                if 'crore' in gb_df['damage'][i] or 'INR' in gb_df['damage'][i] or 'Rs' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
                    te = gb_df['damage'][i].replace('[','').replace(']','')
                    for k in te.split('Rs'):
                        if 'crore' in k:
                            num = k.split('crore')[0].strip(".|'").strip().replace(',','')
                            n = re.findall(r'\d+', num)
                            damages.append(int(n[0]))
                            u = gb_df['url'][i].split('/')[2]
                            if 'www.' in u:
                                u = u.split('.')[1]
                            else:
                                u = u.split('.')[0]
                            site.append(u)
                            month.append(datetime.strptime(gb_df['month_year'][i].split('-')[1], "%Y").year)
                            break
            #     elif 'million' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'million' in k:
            #                 print('$ ',k.split('million')[0].strip(".|'").strip(), ' million')
            #                 break
            #     elif 'billion' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'billion' in k:
            #                 print('$ ',k.split('billion')[0].strip(".|'").strip(' '), ' billion')
            #                 break
            
            except:
                continue

        dam_df = pd.DataFrame({'month':month, 'damages':damages, 'site':site})
        dam_df = dam_df.sort_values(by='month',ascending=False).reset_index(drop=True)
        dam_df = dam_df[dam_df['damages']<11000]
        avg = dam_df.groupby(dam_df['month'])['damages'].transform('mean')

        print(dam_df["month"].tolist())
        #p = sns.scatterplot(data = dam_df, x='month', y='damages', hue='site')
        #sns.lineplot(x = dam_df['month'],y = avg, color='black', alpha=0.3, label='Average')
        #plt.legend(loc='right', bbox_to_anchor=(1.5, 0.5), fontsize='8')
        #plt.xlabel('Month-Year')
        #plt.ylabel('Damages (in Crore)')
        #plt.xticks(rotation=90)
        
        #fig = go.Figure([go.Scatter(x = dam_df['month'], y = dam_df['damages'], mode = 'markers', marker_color = dam_df['site'], \
        #                 line = dict(color = 'firebrick', width = 4))
        #                 ])

        #for x, d in dam_df.groupby('site'):

         #   traces.append(go.Scatter(x=dam_df.month, y=dam_df.damages, name=x))

        #fig = go.Figure(data=traces)
        
        #fig.update_layout(title = 'Estimated Damages',
         #                 xaxis_title = 'Year',
          #                yaxis_title = 'Estimated Damages (in Crore)'
           #               )
           
        fig = px.scatter(dam_df, x="month", y="damages", color="site")
        #fig = go.Figure([go.Scatter(x=dam_df['month'], y=dam_df['damages'], fill=dam_df['site'])])
        fig.add_traces(go.Scatter(x=dam_df['month'], y=avg, mode='lines', name='average'))
        
        
        #fig = px.line(x=month, y=damages, color=site)
        fig.update_layout(
            xaxis=dict(
            type='date',
            title='year'
            )
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    elif dropdown_value == 'Delhi':

        gb_df = pd.read_csv('data/delhi_with_severity.csv')

        gb_df = gb_df[gb_df['category'].notna()]
        gb_df = gb_df[gb_df['category'].str.contains('flood|Flood')]

        gb_df = gb_df[gb_df['location'].notna()]
        gb_df = gb_df[gb_df['location'].str.contains('Delhi')]

        gb_df = gb_df.reset_index()

        month_year = []

        for i in range(len(gb_df['publish date'])):
            if "present" in gb_df['publish date'][i].lower():
                month_year.append('NA')
                continue
            try:
                datee = parser.parse(gb_df['publish date'][i])
            except:
                NOW = datetime.now()
                if 'month' in gb_df['publish date'][i].lower():
                    datee = NOW-relativedelta(months=int(gb_df['publish date'][i].lower().split(' ')[0]))
                elif 'week' in gb_df['publish date'][i].lower():
                    NOW-relativedelta(weeks=int(gb_df['publish date'][i].lower().split(' ')[0]))
            #print(datee)
            month_year.append(str(datee.month) + '-' + str(datee.year))

        gb_df['month_year'] = month_year
                
        month = []
        damages = []
        site = []
        traces=[]
        
        for i in range(gb_df.shape[0]):
            try:
                if 'crore' in gb_df['damage'][i] or 'INR' in gb_df['damage'][i] or 'Rs' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
                    te = gb_df['damage'][i].replace('[','').replace(']','')
                    for k in te.split('Rs'):
                        if 'crore' in k:
                            num = k.split('crore')[0].strip(".|'").strip().replace(',','')
                            n = re.findall(r'\d+', num)
                            damages.append(int(n[0]))
                            u = gb_df['url'][i].split('/')[2]
                            if 'www.' in u:
                                u = u.split('.')[1]
                            else:
                                u = u.split('.')[0]
                            site.append(u)
                            month.append(datetime.strptime(gb_df['month_year'][i].split('-')[1], "%Y").year)
                            break
            #     elif 'million' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'million' in k:
            #                 print('$ ',k.split('million')[0].strip(".|'").strip(), ' million')
            #                 break
            #     elif 'billion' in gb_df['damage'][i]:
            #         print(gb_df['damage'][i])
            #         te = gb_df['damage'][i].replace('[','').replace(']','')
            #         for k in te.split('$'):
            #             if 'billion' in k:
            #                 print('$ ',k.split('billion')[0].strip(".|'").strip(' '), ' billion')
            #                 break
            
            except:
                continue

        dam_df = pd.DataFrame({'month':month, 'damages':damages, 'site':site})
        dam_df = dam_df.sort_values(by='month',ascending=False).reset_index(drop=True)
        dam_df = dam_df[dam_df['damages']<3000]
        avg = dam_df.groupby(dam_df['month'])['damages'].transform('mean')

        print(dam_df["month"].tolist())
        #p = sns.scatterplot(data = dam_df, x='month', y='damages', hue='site')
        #sns.lineplot(x = dam_df['month'],y = avg, color='black', alpha=0.3, label='Average')
        #plt.legend(loc='right', bbox_to_anchor=(1.5, 0.5), fontsize='8')
        #plt.xlabel('Month-Year')
        #plt.ylabel('Damages (in Crore)')
        #plt.xticks(rotation=90)
        
        #fig = go.Figure([go.Scatter(x = dam_df['month'], y = dam_df['damages'], mode = 'markers', marker_color = dam_df['site'], \
        #                 line = dict(color = 'firebrick', width = 4))
        #                 ])

        #for x, d in dam_df.groupby('site'):

         #   traces.append(go.Scatter(x=dam_df.month, y=dam_df.damages, name=x))

        #fig = go.Figure(data=traces)
        
        #fig.update_layout(title = 'Estimated Damages',
         #                 xaxis_title = 'Year',
          #                yaxis_title = 'Estimated Damages (in Crore)'
           #               )
           
        fig = px.scatter(dam_df, x="month", y="damages", color="site")
        #fig = go.Figure([go.Scatter(x=dam_df['month'], y=dam_df['damages'], fill=dam_df['site'])])
        fig.add_traces(go.Scatter(x=dam_df['month'], y=avg, mode='lines', name='average'))
        
        
        #fig = px.line(x=month, y=damages, color=site)
        fig.update_layout(
            xaxis=dict(
            type='date',
            title='year'
            )
        )
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    return fig  

@app.callback(Output(component_id='folium_map', component_property= 'children'),
              [Input(component_id='dropdown', component_property= 'value')])
def folium_map(dropdown_value):
    print(dropdown_value)
    if dropdown_value=='Bengaluru':
        fig = [html.Iframe(name = "folium-map", srcDoc=open('maps/bengaluru_map.html', 'r').read(), style={'width': '600px', 'height': '500px', 'margin-right':'40px', 'border':'none'})]
    elif dropdown_value=='Hyderabad':
        fig = [html.Iframe(name = "folium-map", srcDoc=open('maps/hyderabad_map.html', 'r').read(), style={'width': '600px', 'height': '500px', 'margin-right':'40px', 'border':'none'})]
    elif dropdown_value=='Chennai':
        fig = [html.Iframe(name = "folium-map", srcDoc=open('maps/chennai_map.html', 'r').read(), style={'width': '600px', 'height': '500px', 'margin-right':'40px', 'border':'none'})]
    elif dropdown_value=='Mumbai':
        fig = [html.Iframe(name = "folium-map", srcDoc=open('maps/mumbai_map.html', 'r').read(), style={'width': '600px', 'height': '500px', 'margin-right':'40px', 'border':'none'})]
    elif dropdown_value=='Delhi':
        fig = [html.Iframe(name = "folium-map", srcDoc=open('maps/delhi_map.html', 'r').read(), style={'width': '600px', 'height': '500px', 'margin-right':'40px', 'border':'none'})]
    return fig  

if __name__ == '__main__': 
    app.run(debug=True)

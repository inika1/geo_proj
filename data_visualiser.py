import pycountry
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import gzip,numpy as np, pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import pycountry
import base64
import dash_bootstrap_components as dbc
import datetime
import io
import dash_table
from pycountry import countries
import pandas as pd

us_states= {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
us_states = {k.upper():v.upper() for k,v in us_states.items()}

def clean_df(temp):
    df = temp.iloc[: , :40]
    for i in df.columns.tolist():
        if len(pd.to_numeric(df[i], 'coerce').dropna()) > (len(df[i])/4):
            df[i] = pd.to_numeric(df[i], 'coerce')

    df.replace("nd", np.nan,inplace=True)
    df.replace("na", np.nan,inplace=True)
    df.replace("-", np.nan,inplace=True)
    df.replace(" -", np.nan,inplace=True)

    count_state = 0
    count_country = 0
    
    for i in df.columns.tolist():
        state_codes = []
        country_codes = []
        var = 0
        for y in df[i]:
            if isinstance(y, str):
                if list(us_states.keys()).count(y.upper()) > 0:
                    count_state = count_state+1
                elif list(us_states.values()).count(y.upper()) > 0:
                    count_state = count_state+1
                
                else: 
                    try: 
                        countries.get(alpha_3 = y).name
                        count_country = count_country+1
                    except:
                        var = 0


                    try: 
                        countries.get(name = y).name
                        count_country = count_country+1
                    except:
                        var = 0


        
        
        if count_state > (len(df[i])/4):
            for y in df[i]:
                try:
                    if list(us_states.keys()).count(y.upper()) > 0:
                        state_codes.append(us_states.get(y.upper()))
                    else:
                        state_codes.append(y.upper())
                except:
                    state_codes.append(y)
            try:
                df[i + '_statecodes'] = state_codes
            except:
                var = 0

        elif count_country > (len(df[i])/4):
            for y in df[i]:
                try: 
                    y = countries.get(alpha_3 = y).name.lower()
                except:
                    var = 0

                try: 
                    y = countries.get(name = y).name.lower()
                except:
                    var = 0
                country_codes.append(y)
            df[i + '_countrycodes'] = country_codes

        count_state = 0
        count_country = 0
    
    return df

df = clean_df(pd.read_csv('demo_data1.csv', dtype = str))

df_data2 = clean_df(pd.read_csv('demo_data2.csv', dtype = str))

df_data1 = df


app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


plottypes = ['histogram','scatter','map']
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    global df
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            new_df = pd.read_csv(io.StringIO(decoded.decode('utf-8')),dtype=str)
            
            
            
            df = clean_df(new_df)
            
            return df

        
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


app.layout = html.Div([
    html.Div([html.H3(children = "Data visualisation of CSV files", className = "text-center text-light",style={
                'margin-left': '10px',  'margin-top': '10px', 'display': 'inline-block', 'font-weight': '500'}),html.A(
                id='gh-link',
                children=[
                    'View on GitHub'
                ],
                href="https://github.com/inika1/geo_proj",style={'color': 'white',
                       'border': 'solid 1px white',
                       'text-decoration': 'none',
                       'font-size': '10pt',
                       'font-family': 'sans-serif',
                       'color': '#fff',
                       'border': 'solid 1px #fff',
                       'border-radius': '2px',
                                        'padding': '2px',
                                        'padding-top': '5px',
                                        'padding-left': '15px',
                                        'padding-right': '15px',
                                        'font-weight': '100',
                                        'position': 'relative',
                                        'top': '15px',
                                        'float': 'right',
                                        'margin-right': '40px',
                                        'margin-left': '5px',
                                        'transition-duration': '400ms',
                       }
             
            ),html.Div(
                className="div-logo",
                children=html.Img(
                    className="logo", src=("https://opendatabim.io/wp-content/uploads/2021/12/GitHub-Mark-Light-64px-1.png"),
                    style={'height': '48px',
                           'padding': '6px', 'margin-top': '3px'}
                ), style={'display': 'inline-block', 'float': 'right'}
            ),],className="bg-primary bg-opacity-75 mt-0 mb-3 p-4"),
    
   
    dbc.Row([dbc.Col(html.H6(children = "Upload a CSV file:",style = {'margin': '10px'})), dbc.Col( html.H6(children = "Or pick a demo dataset:",style = {'margin': '10px'}))]),
    dbc.Row([dbc.Col([
            dcc.Upload(
        id="upload-data",
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File',style={"textDecoration": "underline", "cursor": "pointer"}, id = "tooltip")]),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }),dbc.Tooltip("Refresh page after upload! File should be less than 10mb, contain numerical data (eg age or bmi) and contain locations(countries or USA states) to use all the plotting functions", 
            target="upload-data",placement="top",style={'color': 'white',
                       'font-size': '10pt',
                       'font-family': 'sans-serif',
                       'color': '#fff'}
        )]), dbc.Col(
    dcc.Dropdown(['dataset1','dataset2'], value = 'dataset1', id = "demo", clearable = True,style = {'margin-right': '10px'}),align="center")]),
    
    
    
    dbc.Row([dbc.Col(
    html.Div(children = [
    dcc.Graph(id="graph1")
    ])),
    

    dbc.Col( html.Div([html.Hr(),html.H6(children = 'Select plot type:'),html.Br(),dcc.RadioItems(plottypes,'histogram', id="graphDropdown",labelStyle={'display': 'inline-block'},inputStyle={"margin-right": "10px", "margin-left":"10px"}),
              html.Br(),html.H6(children = 'Select variable 1:'),html.Br(),
              dcc.Dropdown(id= "dropdown",options = [],value=None,clearable=True),html.Br(),html.H6(children = 'Select variable 2:'),html.Br(), 
              dcc.Dropdown(id= "dropdown2",options=[],value=None,clearable=True)],className = "bg-light"),width=3),
             
    
    dbc.Col(html.Div([html.Hr(),html.H6(children = 'Group by:'),html.Br(),dcc.Dropdown(id = 'groupby', options=[],value=None,clearable=True),html.Br(),
                        html.H6(children = 'Select condition for map:'),html.Br(),
                        dcc.Dropdown(id = "map_options",options=[],value=None,clearable=True, multi = True)], className = "bg-light"),width=3) ], className = "bg-light",style={'margin': '10px'}),
    
    
    html.Div(id = 'placeholder'),
])

@app.callback(
    Output('placeholder', "children"),
    [Input('upload-data', 'contents'), Input('demo','value')],
    State('upload-data', 'filename'))
def update_options(content,value,name):
    global df
    if content is not None:
        df = parse_contents(content, name)
    
    else: 
        if value == 'dataset1':
            global df_data1

            df = df_data1
        elif value == 'dataset2':
            global df_data2
            df = df_data2


    return []

@app.callback(
    Output("dropdown", "options"),
    Output("dropdown", "value"),
    [Input("graphDropdown","value")])

def update_options(value):
    global df
    if value == 'histogram':
        options = [{'label': i, 'value': i} for i in df.columns.tolist() if ('_statecodes' not in i) and ('_countrycodes' not in i) and (len(df[i].unique())>1) and (len(df[i].value_counts().unique()) > 1)]
        
    elif value == 'scatter':
        options = []
        for i in df.columns.tolist():
             if df[i].dtype == 'float64' or df[i].dtype == 'int64':
                    options.append({'label': i, 'value': i})
        if len(options)<2:
            options = []

    else:
        options = []
        for i in df.columns.tolist():
            if '_statecodes' in i:
                    options.append({'label': i.replace('_statecodes',''), 'value': i})
            elif '_countrycodes' in i:
                  options.append({'label': i.replace('_countrycodes',''), 'value': i})
    


    try:
        return options,options[0].get("value")
    except:
        return options, None
    

@app.callback(
    Output('demo', "value"),
    [Input('dropdown','options')])

def update_options(options2):
    global df
    
    global df_data1
    
    global df_data2

    if df.columns.tolist() != (df_data1.columns.tolist()):
        if df.columns.tolist() != (df_data2.columns.tolist()):
            return None
        else:
            return 'dataset2'
    
    else:
        return 'dataset1'

@app.callback(
    Output("dropdown2", "options"),
    Output("dropdown2", "value"),
    [Input("graphDropdown","value"),Input("dropdown", "value")])
def update_options(value,value2):
    global df
    if value == 'scatter':
        options = []
        for i in df.columns.tolist():
                if df[i].dtype == 'float64' or df[i].dtype == 'int64' :
                    if i != value2:
                        options.append({'label': i, 'value': i})
        if len(options)<2:
            options = []
        return options, None
    else:
        return [], None


@app.callback(
    Output("groupby", "options"),
    Output("groupby", "value"),
    [Input("dropdown", "value"), Input("dropdown2","value"),Input("graphDropdown","value") ])

def update_options(value,value2,graph):
    global df
    options = []
    
    df1 = df.dropna(subset = [value], inplace = False)
    
    if graph == 'scatter':
        if value2 is not None:
            df1 = df1.dropna(subset = [value2], inplace = False)

            for i in df1.columns.tolist():
                df_temp = df1.dropna(subset = [i], inplace = False)
                if len(df_temp[i].unique()) > 1 and len(df_temp[i].unique()) < 7:
                    if i != value2 and i !=value:
                        options.append({'label': i, 'value': i})
    else:
        
        for i in df1.columns.tolist():
            df_temp = df1.dropna(subset = [i], inplace = False)
            if len(df_temp[i].unique()) > 1 and len(df_temp[i].unique()) < 7:
                if i !=value:
                    options.append({'label': i, 'value': i})
    
    
    return options,None
 
       
        
@app.callback(
    Output("map_options", "options"),Output("map_options", "value"),
    [Input("graphDropdown","value"),Input("groupby", "value")])

def update_options(graph,value):
    global df
    if graph == 'map':
        options = []
        df_map = df.dropna(subset = [value], inplace = False)
        for i in df_map[value].unique():
                options.append({'label': i, 'value': i})
        return options, None
    else:
        return [], None


@app.callback(
    Output("graph1", "figure"), 
    [Input("dropdown", "value"), Input("dropdown2", "value"), Input("graphDropdown","value"), Input("groupby","value"), Input("map_options","value")])


def plot(value,value3,value2,grp,m_option):
    global df
    if value2 == 'histogram':
        df_histo = df.dropna(subset = [value], inplace = False)
        grouptype = "group"

        if grp is not None:
            df_histo = df_histo.dropna(subset = [grp])

            if df[value].dtype == 'float64' or df[value].dtype == 'int64':
                if len(df[grp].unique()) > 3:
                    grouptype = "overlay"
                else:
                    
                    grouptype = "stack"

        try:
            fig = px.histogram(df_histo, x=value, color = grp, barmode = grouptype)
        except:
            fig = px.histogram(df_histo, x=value, color = grp, barmode = grouptype)

        fig = fig.update_layout(
        plot_bgcolor= '#FFFFFF',
        paper_bgcolor='#FFFFFF'
        )
        fig = fig.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
        fig = fig.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
        


    elif value2 == 'scatter':

        
        if grp is not None:
            df_scatter = df.dropna(subset = [grp])
            fig = px.scatter(df_scatter, x=value, y=value3, trendline='ols', color=grp)
        else:
            fig = px.scatter(df, x=value, y=value3, trendline='ols')

        fig = fig.update_layout(
            plot_bgcolor= '#FFFFFF',
            paper_bgcolor='#FFFFFF'
         )
        fig = fig.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
        fig = fig.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')

       


    else:
        temp = df
        if m_option is not None:

            if m_option != []:

                  temp = df[df[grp].isin(m_option)]

        df_geo = temp[value].value_counts().rename_axis(value).reset_index(name='Count')

        if '_statecodes' in value:
            fig = px.choropleth(df_geo,locations = value,color = 'Count',locationmode = "USA-states",scope="usa")
        else:
            fig = px.choropleth(df_geo,locations = value,color = 'Count',locationmode = 'country names')

    return fig




        
           
        

    



#if __name__ == "__main__":
    #app.run_server(debug=True,use_reloader=False,port=8049)

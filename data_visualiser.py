from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import gzip,numpy as np, pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

import base64
import datetime
import io

import dash_table

import pandas as pd
df = pd.DataFrame()

app = Dash(__name__)

plottypes = ['histogram','scatter','map']
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    global df
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            new_df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            df = new_df.copy()
            for i in df.columns.tolist():
                if len(pd.to_numeric(df[i], 'coerce').dropna()) > (len(df[i])/4):
                    df[i] = pd.to_numeric(df[i], 'coerce')
            
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

app.layout = html.Div([
    dcc.Upload(
        id="upload-data",
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    
    html.Div(children = [
    dcc.Graph(id="graph1")
    ], style={'width': '49%','display': 'inline-block',"verticalAlign": "top"}),
   
   html.Div(children = [ html.H5(children = 'Select plot type'),dcc.Dropdown(plottypes,'histogram', id="graphDropdown"),
              html.H5(children = 'Select variable 1'), 
              dcc.Dropdown(id= "dropdown",options=[],value=None,clearable=True),html.H5(children = 'Select variable 2'), 
              dcc.Dropdown(id= "dropdown2",options=[],value=None,clearable=True)]
             ,style={'width': '24%','display': 'inline-block',"verticalAlign": "top"}),
    
    html.Div(id = 'placeholder')
])

@app.callback(
    Output('placeholder', "children"),
    [Input('upload-data', 'contents')],
    State('upload-data', 'filename'))
def update_options(content,name):
    global df
    if content is not None:
        df = parse_contents(content, name)
    return []

@app.callback(
    Output("dropdown", "options"),
    [Input("graphDropdown","value")])

def update_options(value):
    global df
    if value == 'histogram':
        options = [{'label': i, 'value': i} for i in df.columns.tolist()]
    elif value == 'scatter':
        options = []
        for i in df.columns.tolist():
             if df[i].dtype == 'float64' or df[i].dtype == 'int64':
                    options.append({'label': i, 'value': i})
    return options

@app.callback(
    Output("dropdown2", "options"),
    [Input("graphDropdown","value")])
def update_options(value):
    global df
    if value == 'scatter':
        options = []
        for i in df.columns.tolist():
                if df[i].dtype == 'float64' or df[i].dtype == 'int64' :
                    options.append({'label': i, 'value': i})
        return options
    else:
        return []

@app.callback(
    Output("graph1", "figure"),
    [Input("dropdown", "value"), Input("dropdown2", "value"), Input("graphDropdown","value")])


def plot(value,value3,value2):
    global df
    if value2 == 'histogram':
        fig = px.histogram(df, x=value,barmode="stack")
    elif value2 == 'scatter':
        fig = px.scatter(df,x=value,y=value3)
    fig = fig.update_layout(
        plot_bgcolor= '#FFFFFF',
        paper_bgcolor='#FFFFFF'
    )
    fig = fig.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
    fig = fig.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
        
    return fig

#if __name__ == "__main__":
    #app.run_server(debug=True,use_reloader=False,port=8049)

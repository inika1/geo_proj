from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import gzip,numpy as np, pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import geopandas as gpd

app = Dash(__name__)


df = pd.read_csv('/home/inika1/mysite/abundance.txt',sep="\t",dtype=object,header=None).T

df.columns=df.iloc[0,:]
df=df.iloc[1:]
df.index=df['country']
df.age = pd.to_numeric(df.age, 'coerce')
df.age[df.age == df.age // 1]
df.bmi = pd.to_numeric(df.bmi, 'coerce')
df['disease'].mask(df['disease'] == "obese","obesity", inplace=True)

df_disease = df[(df.disease != "nd") & (df.disease != "n")  & (df.gender != "nd") &(df.gender != "-") & (df.gender != " -")]
df_age = df[(df.gender != "nd") &(df.gender != "-") & (df.gender != " -") & (df.gender != "na")]

fig1 = px.histogram(df_disease, x="disease",color = "gender",barmode="group", color_discrete_map={"male": "blue", "female": "pink"},)
fig1 = fig1.update_layout(
    plot_bgcolor= '#FFFFFF',
    paper_bgcolor='#FFFFFF'
)
fig1 = fig1.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
fig1 = fig1.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')

diseases = ['all','no disease', 't2d','obesity','ibd_ulcerative_colitis','cirrhosis','leaness','stec2-positive','impaired_glucose_tolerance','cancer','n_relative','y','small_adenoma','ibd_crohn_disease','large_adenoma','overweight','underweight']

app.layout = html.Div(children=[

    html.Div(children = [
        dcc.Dropdown(diseases, 'all', id ="dropdown"),
        dcc.Graph(
        id="graph3"), 
        dcc.Graph(
        id="graph2")],
        style={'width': '49%','display': 'inline-block','padding': '0 20'}),
    
    html.Div(children = [
    dcc.Graph(
        id="graph4"),
    dcc.Graph(
        id='disease histogram',
        figure=fig1)],
        style={'width': '49%','display': 'inline-block','padding': '0 20'}),  
    
    
])

@app.callback(
    Output("graph4", "figure"),
    Input("dropdown", "value"))

def plot_age_histogram(value):
    df1 = df_age
    if value != "all":
            if value == "no disease":
                df1 = df_age[(df_age.disease == "n") | (df_age.disease == "nd")]
            else: 
                df1 = df_age[(df_age.disease == value)]

    fig = px.histogram(df1, x="age",color = "gender",barmode="stack", color_discrete_map={"male": "powderblue", "female": "violet"},)
    fig = fig.update_layout(
        plot_bgcolor= '#FFFFFF',
       paper_bgcolor='#FFFFFF'
     )
    fig = fig.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
    fig = fig.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
    return fig


@app.callback(
    Output("graph2", "figure"),
    Input("dropdown", "value"))

def plot_map(value):
    df2 = df
    if value != "all":
            if value == "no disease":
                df2 = df[(df.disease == "n") | (df.disease == "nd") ]
            else: 
                df2 = df[(df.disease == value)]
    
    df_country = df2['country'].value_counts().rename_axis('country') .reset_index(name='Number of People')
    fig = px.choropleth(df_country,locations = 'country',color = 'Number of People', locationmode = 'country names',color_continuous_scale="sunsetdark")
    fig = fig.update_geos(
        resolution=110,
        showland=True, landcolor="white",
        showocean=True, oceancolor="LightBlue",
        projection_type="natural earth"

     )
    fig = fig.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@app.callback(
    Output("graph3", "figure"),
    Input("dropdown", "value"))

def plot_scatter(value):
    
    df_bmi = df[(df.bmi != "n") & (df.bmi != "nd")& (df.gender != "nd") & (df.gender != "na")]
    df_bmi['bmi'] = df_bmi['bmi'].astype('float')
    
    df2 = df_bmi
    
    if value != "all":
            if value == "no disease":
                df2 = df_bmi[(df_bmi.disease == "n") | (df_bmi.disease == "nd") ]
            else: 
                df2 = df_bmi[(df_bmi.disease == value)]
    
    fig = px.scatter(df2.dropna(),x="age",y="bmi",color="gender", color_discrete_map={"male": "blue", "female": "red"}, labels={"age":"Age", "bmi":"BMI"})
    fig = fig.update_layout(
       plot_bgcolor= '#FFFFFF',
       paper_bgcolor='#FFFFFF'
     )
    fig = fig.update_xaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
    fig = fig.update_yaxes(showline=True, linewidth=1, linecolor='black',gridcolor='#d3d3d3')
    return fig



# if __name__ == '__main__':
#     app.run_server(debug=True,use_reloader=False,port=8049)

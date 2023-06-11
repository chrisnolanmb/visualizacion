import data
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Read in dataframes
df_lic = data.df_lic
df_master = data.df_master
df_doc = data.df_doc

# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Licenciatura', value='tab-1'),
        dcc.Tab(label='Maestría', value='tab-2'),
        dcc.Tab(label='Doctorado', value='tab-3')
    ]),
    html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='maps')
        ])
])

# Define the callback function
@app.callback(Output('maps', 'figure'),
              Input('tabs', 'value'))

def render_content(tab):
    if tab == 'tab-1':
        df = df_lic
        df_lic['size'] = 10
        fig = px.scatter_mapbox(df, 
                                lat=df["lat"], 
                                lon=df.lon, 
                                zoom=4.7, 
                                height=800,
                                # width=900,
                                center={"lat": 23.6345, "lon": -102.5528},
                                hover_data=[df.Correo,
                                            df["Nombre de la Carrera (Licenciatura)"],
                                            df["Institución/Universidad"],
                                            df["Sede (Licenciatura)"],
                                            df["Página web del programa de Licenciatura (si hubiera)"],
                                            df["Entidad Federativa donde se imparte"],
                                            df["¿Su Institución tiene un programa Nivel Licenciatura?"],
                                            df["Dirección física (Licenciatura)"],
                                            df["Área(s) de interés (Licenciatura)"],
                                            df["¿La Institución es pública o privada?"]],
                                size=df["size"]
                                                                                                # mapbox_style = 'stamen- terrain'
                                            )
    elif tab == 'tab-2':
        df = df_master
        df_master['size'] = 10
        fig = px.scatter_mapbox(df, 
                                lat=df["lat"], 
                                lon=df.lon, 
                                zoom=4.7, 
                                height=800,
                                center={"lat": 23.6345, "lon": -102.5528},
                                hover_data=[df.Correo],
                                size=df_master["size"])
    else:
        df = df_doc
        df_doc['size'] = 10
        fig = px.scatter_mapbox(df, 
                                lat=df["lat"], 
                                lon=df.lon, 
                                zoom=4.7, 
                                height=800,
                                center={"lat": 23.6345, "lon": -102.5528},
                                hover_data=[df.Correo],
                                color_discrete_sequence=["fuchsia"],
                                size=df_doc["size"])

    # fig = px.scatter_mapbox(df, lat=df["lat"], lon=df["lon"], hover_name="Institución/Universidad", hover_data=["Entidad Federativa donde se imparte"], zoom=4,
    #                         color_discrete_sequence=["fuchsia"], height=500)
    
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)
import data
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Read in dataframes
df_lic = data.df_lic
df_master = data.df_master
df_doc = data.df_doc

# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}
estados = data.estados_dict

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = dbc.Container(
    [
        html.H1("Mapa de Programas Educativos"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Tabs(id='tabs', value='tab-1', children=[
                            dcc.Tab(label='Licenciatura', value='tab-1'),
                            dcc.Tab(label='Maestría', value='tab-2'),
                            dcc.Tab(label='Doctorado', value='tab-3')
                        ]),
                        dcc.Graph(figure={}, id='maps')
                    ],
                    width=6
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Selecciona un Estado"),
                                        dcc.Dropdown(
                                            id="estado",
                                            options=[
                                                {"label": col, "value": col} for col in estados
                                            ],
                                            value="",
                                        ),
                                    ]
                                ),
                            ],
                            body=True,
                        )
                    ],
                    width=6
                ),
            ],
            justify="between",
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output('maps', 'figure'),
    [
        Input('tabs', 'value'),
        Input('estado', 'value')
    ],
)
def render_content(tab, estado):
    if tab == 'tab-1':
        df = df_lic
        df_lic['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=800,
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
                                size=df["size"],
                                color_discrete_sequence=["green"]
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
                                size=df_master["size"],
                                color_discrete_sequence=["orange"])
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
                                color_discrete_sequence=["red"],
                                size=df_doc["size"])

    if estado is not None:
        df_estado = df[df['Entidad Federativa donde se imparte'] == estado]
        if len(df_estado) > 0:
            fig.update_layout(
                mapbox_center={"lat": df_estado['lat'].mean(
                ), "lon": df_estado['lon'].mean()}
            )
            fig.update_layout(mapbox_zoom=6)
            fig.update_mapboxes(
                zoom=9,
                style='open-street-map',
                center=dict(lat=df_estado['lat'].mean(),
                            lon=df_estado['lon'].mean())
            )
            fig.update_layout(
                mapbox={
                    'center': {'lat': df_estado['lat'].mean(), 'lon': df_estado['lon'].mean()},
                    'zoom': 9,
                    'style': 'open-street-map'
                }
            )
        else:
            fig.update_layout(
                mapbox_center={"lat": 23.6345, "lon": -102.5528}
            )
            fig.update_layout(mapbox_zoom=4.2)
            fig.update_mapboxes(
                zoom=4.2,
                style='open-street-map',
                center=dict(lat=23.6345, lon=-102.5528)
            )
            fig.update_layout(
                mapbox={
                    'center': {'lat': 23.6345, 'lon': -102.5528},
                    'zoom': 4.2,
                    'style': 'open-street-map'
                }
            )
    else:
        fig.update_layout(
            mapbox_center={"lat": 23.6345, "lon": -102.5528}
        )
        fig.update_layout(mapbox_zoom=4.2)
        fig.update_mapboxes(
            zoom=4.2,
            style='open-street-map',
            center=dict(lat=23.6345, lon=-102.5528)
        )
        fig.update_layout(
            mapbox={
                'center': {'lat': 23.6345, 'lon': -102.5528},
                'zoom': 4.2,
                'style': 'open-street-map'
            }
        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)

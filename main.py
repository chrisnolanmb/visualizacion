import data
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# leer los dataframe de las licenciaturas, maestrias y doctorados
df_lic = data.df_lic
df_master = data.df_master
df_doc = data.df_doc

# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}
estados = data.estados_dict

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #fca311',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': '#E5E5E5',
    
    'backgroundColor': '#000000'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#14213d',
    'color': 'white',
    'padding': '6px'
}

#se cran las tarjetas que contendran la informacion mas relevante
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P("This card has some text content, but not much else"),
            dbc.Button("Go somewhere", color="primary"),
        ]
    )
)


second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This card also has some text content and not much else, but "
                "it is twice as wide as the first card."
            ),
            dbc.Button("Go somewhere", color="primary"),
        ]
    )
)

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
                                dbc.CardBody(id="stats")
                            ],
                            body=True,
                        )
                    ],
                    width={'size': 12, 'order': 2},
                    lg={'size': 6, 'order': 2}
                ),
                dbc.Col(
                    [
                        dcc.Tabs(id='tabs', 
                                 value='tab-1',
                                                              
                                 children=[
                            dcc.Tab(label='Licenciatura', 
                                    value='tab-1',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    style=tab_style, 
                                    selected_style=tab_selected_style),
                            dcc.Tab(label='Maestría',
                                    value='tab-2',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    style=tab_style, 
                                    selected_style=tab_selected_style),
                            dcc.Tab(label='Doctorado', 
                                    value='tab-3',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    style=tab_style, 
                                    selected_style=tab_selected_style)
                        ]),
                        dcc.Graph(figure={}, id='maps')
                    ],
                    width={'size': 12, 'order': 1},
                    lg={'size': 6, 'order': 1}
                ),
            ],
            justify="between",
            align="center",
        ),
        dbc.Row(
            html.Div(
            [
                dbc.Card(
                    dbc.CardBody("This is some text within a card body"),
                    className="mb-3",
                ),
                dbc.Card("This is also within a body", id='stats', body=True),
            ]
            )
        ),
        dbc.Row(
        [
            dbc.Col(first_card, width=4),
            dbc.Col(second_card, width=8),
        ]
        ),
    ],
    fluid=True,
)

@app.callback(
    Output('estado', 'options'),
    [Input('tabs', 'value')]
)
def update_dropdown_options(tab):
    if tab == 'tab-1':
        df = df_lic
    elif tab == 'tab-2':
        df = df_master
    else:
        df = df_doc

    entidad_options = [{'label': entidad, 'value': entidad}
                       for entidad in df['Entidad Federativa donde se imparte'].unique()]

    return entidad_options


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
                                            # df["Sede (Licenciatura)"],
                                            df["Página web del programa de Licenciatura (si hubiera)"],
                                            df["Entidad Federativa donde se imparte"],
                                            # df["¿Su Institución tiene un programa Nivel Licenciatura?"],
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
                                hover_data=[df["Dirección física (Doctorado)"]],
                                color_discrete_sequence=["red"],
                                size=df_doc["size"])

    if estado is not None:
        df_estado = df[df['Entidad Federativa donde se imparte'] == estado]

        if len(df_estado) > 0:
            zoom_level = 9 if estado != 'Tamaulipas' else 7

            fig.update_mapboxes(
                domain={'x': [0, 1], 'y': [0, 1]},
                center=dict(lat=df_estado['lat'].mean(),
                            lon=df_estado['lon'].mean()),
                zoom=zoom_level,
                style='open-street-map',
                bearing=0
            )

            fig.update_layout(
                mapbox_center={"lat": float(df_estado['lat'].iloc[0]),
                               "lon": float(df_estado['lon'].iloc[0])}

            )
            fig.update_layout(mapbox_zoom=6)
            fig.update_mapboxes(
                zoom=8,
                style='open-street-map',
                center=dict(lat=df_estado['lat'].mean(),
                            lon=df_estado['lon'].mean())
            )
            fig.update_layout(
                mapbox={
                    'center': {'lat': df_estado['lat'].mean(), 'lon': df_estado['lon'].mean()},
                    'zoom': 8,
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
#Esto aun no funciona xD
        fig.update_traces(
            hovertemplate="<b>%{text}</b><br>"
                  "Correo: %{customdata[0]}<br>"
                  "Carrera: %{customdata[1]}<br>"
                  "Institución: %{customdata[2]}<br>"
                  "Página web: %{customdata[3]}<br>"
                  "Entidad Federativa: %{customdata[4]}<br>"
                  "Dirección: %{customdata[5]}<br>"
                  "Área(s) de interés: %{customdata[6]}<br>"
                  "Pública o privada: %{customdata[7]}<br>"
        )

    return fig


@app.callback(
    Output('stats', 'children'),
    [Input('estado', 'value')]
)


def update_stats(estado):
    '''
    Esta funcion se encarga de actualizar las estadisticas de la entidad federativa seleccionada
    '''
    if estado is not None:
        df_estado = df_lic[df_lic['Entidad Federativa donde se imparte'] == estado]
        total_licenciaturas = len(df_estado)
        total_instituciones = len(df_estado['Institución/Universidad'].unique())

        return [
            html.H3(f"Estadísticas del estado seleccionado ({estado})"),
            html.P(f"Total de Licenciaturas: {total_licenciaturas}"),
            html.P(f"Total de Instituciones: {total_instituciones}"),
            html.P(f"Total de Instituciones Públicas: {len(df_estado[df_estado['¿La Institución es pública o privada?'] == 'Pública'])}"),
            html.P(f"Total de Instituciones Privadas: {len(df_estado[df_estado['¿La Institución es pública o privada?'] == 'Privada'])}"),
            html.P(f"Areas de interes más comunes: {', '.join(df_estado['Área(s) de interés (Licenciatura)'].value_counts().head(1).index.unique())}"),
            html.P(f"interesadas en Ciencias de datos: {len(df_estado[df_estado['Área(s) de interés (Licenciatura)'].str.contains('Ciencia de datos')])}"),

            # Agrega más componentes para mostrar otras estadísticas
        ]
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)

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

# se cran las tarjetas que contendran la informacion mas relevante
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
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    'style.css'
]
)

# Define the app layout
# app.layout = dbc.Container(

#     [

#         html.H1("Mapa de Programas Educativos"),
#         dbc.Row(
#     [
#         dbc.Col(
#             [
#                 dbc.Card(
#                     [
#                         html.Div(className="dropdown", children=
#                             [
#                                 dbc.Label("Selecciona un Estado"),
#                                 dcc.Dropdown(
#                                     id="estado",
#                                     options=[
#                                         {"label": col, "value": col} for col in estados
#                                     ],
#                                     value="",
#                                 ),
#                             ]
#                         ),

#                     ],
#                     body=True,
#                 )
#             ],
#             width={'size': 4, 'order': 2},  # Ajusta el ancho de la columna del dropdown
#             lg={'size': 3, 'order': 2}
#         ),
#         dbc.Col(
#             [
#                 dcc.Tabs(id='tabs',
#                          value='tab-1',
#                          className='custom-tabs',
#                          children=[
#                              dcc.Tab(label='Licenciatura',
#                                      value='tab-1',
#                                      className='custom-tab',
#                                      selected_className='custom-tab--selected'
#                                      ),
#                              dcc.Tab(label='Maestría',
#                                      value='tab-2',
#                                      className='custom-tab',
#                                      selected_className='custom-tab--selected'
#                                      ),
#                              dcc.Tab(label='Doctorado',
#                                      value='tab-3',
#                                      className='custom-tab',
#                                      selected_className='custom-tab--selected'
#                                      )
#                          ]),
#                 dcc.Graph(figure={}, id='maps')
#             ],
#             width={'size': 8, 'order': 1},  # Ajusta el ancho de la columna del mapa
#             lg={'size': 9, 'order': 1}
#         ),
#     ],
#     justify="between",
#     align="center",
# ),
#         # dbc.Row(
#         #     html.Div(
#         #     [
#         #         dbc.Card(
#         #             dbc.CardBody("This is some text within a card body"),
#         #             className="mb-3",
#         #         ),
#         #         dbc.Card("This is also within a body", id='stats', body=True),
#         #     ]
#         #     )
#         # ),
#         # dbc.Row(
#         #     [

#         #         dbc.Col(first_card, width=4),
#         #         dbc.Col(second_card, width=8),
#         #     ]
#         # ),
#         dbc.Row(
#             [
#                 dbc.Col(id="stats"),
#             ]
#         ),

#     ],
#     fluid=True,
# )

# app.layout = dbc.Container(
#     [
#         html.H1("Mapa de Programas Educativos"),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         dbc.Card(
#                             [
#                                 html.Div(className="dropdown", children=
#                                     [
#                                         dbc.Label("Selecciona un Estado"),
#                                         dcc.Dropdown(
#                                             id="estado",
#                                             options=[
#                                                 {"label": col, "value": col} for col in estados
#                                             ],
#                                             value="",
#                                         ),
#                                     ]
#                                 ),

#                             ],
#                             body=True,
#                         ),
#                         dbc.Row(
#                             [
#                                 dbc.Col(first_card, width=6),
#                                 dbc.Col(second_card, width=6),
#                             ],
#                             className="mb-3",
#                         ),
#                         dbc.Row(
#             [
#                 dbc.Col(id="stats"),
#             ]
#         ),
#                     ],
#                     width={'size': 4, 'order': 2},
#                     lg={'size': 3, 'order': 2}
#                 ),
#                 dbc.Col(
#                     [
#                         dcc.Tabs(id='tabs',
#                                  value='tab-1',
#                                  className='custom-tabs',
#                                  children=[
#                                      dcc.Tab(label='Licenciatura',
#                                              value='tab-1',
#                                              className='custom-tab',
#                                              selected_className='custom-tab--selected'
#                                              ),
#                                      dcc.Tab(label='Maestría',
#                                              value='tab-2',
#                                              className='custom-tab',
#                                              selected_className='custom-tab--selected'
#                                              ),
#                                      dcc.Tab(label='Doctorado',
#                                              value='tab-3',
#                                              className='custom-tab',
#                                              selected_className='custom-tab--selected'
#                                              )
#                                  ]),
#                         dcc.Graph(figure={}, id='maps')
#                     ],
#                     width={'size': 8, 'order': 1},
#                     lg={'size': 9, 'order': 1}
#                 ),
#             ],
#             justify="between",
#             align="center",
#         ),
#     ],
#     fluid=True,
# )
app.layout = dbc.Container(
    [
        html.H1("Mapa de Programas Educativos"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.Div(className="dropdown", children=[
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
                        ),
                        dbc.Row(
                            [
                                dbc.Col(first_card, width=6),
                                dbc.Col(second_card, width=6),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(id="stats"),
                            ]
                        ),
                    ],
                    # Adjust the width of the column
                    width={'size': 12, 'order': 'first'},
                    lg={'size': 4, 'order': 'first'}
                ),
                dbc.Col(
                    [
                        dcc.Tabs(id='tabs',
                                 value='tab-1',
                                 className='custom-tabs',
                                 children=[
                                     dcc.Tab(label='Licenciatura',
                                             value='tab-1',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected'
                                             ),
                                     dcc.Tab(label='Maestría',
                                             value='tab-2',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected'
                                             ),
                                     dcc.Tab(label='Doctorado',
                                             value='tab-3',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected'
                                             )
                                 ]),
                        dcc.Graph(figure={}, id='maps', config={
                                  'displayModeBar': False})
                    ],
                    # Adjust the width of the column
                    width={'size': 12, 'order': 'last'},
                    lg={'size': 8, 'order': 'last'},
                ),
            ],
            justify="between",
            align="center",
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
                                hover_data=[
                                    # df.Correo,
                                    # df["Nombre de la Carrera (Licenciatura)"],
                                    # df["Institución/Universidad"],
                                    # df["Sede (Licenciatura)"],
                                    # df["Página web del programa de Licenciatura (si hubiera)"],
                                    # df["Entidad Federativa donde se imparte"],
                                    # df["¿Su Institución tiene un programa Nivel Licenciatura?"],
                                    df["Dirección física (Licenciatura)"],
                                    # df["Área(s) de interés (Licenciatura)"],
                                    # df["¿La Institución es pública o privada?"]]
                                ],
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
                                hover_data=[
                                    df["Dirección física (Doctorado)"]],
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
        total_instituciones = len(
            df_estado['Institución/Universidad'].unique())

        return [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    f"Estadísticas del estado seleccionado ({estado})"),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"Total de Licenciaturas: {total_licenciaturas}"),
                                    ]
                                ),
                            ]
                        ),
                        width=5  # Ancho de la columna
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Total de Instituciones"),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"Total de Instituciones: {total_instituciones}"),
                                    ]
                                ),
                            ]
                        ),
                        width=4  # Ancho de la columna
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    "Total de Instituciones Públicas"),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            f"Total de Instituciones Públicas: {len(df_estado[df_estado['¿La Institución es pública o privada?'] == 'Pública'])}"),
                                    ]
                                ),
                            ]
                        ),
                        width=4  # Ancho de la columna
                    ),
                ]
            ),
            dbc.Card(className="glassmorphism", children=[

                html.H5("Total de Instituciones Públicas:",
                        className="card-title"),
                html.P(
                    f"{len(df_estado[df_estado['¿La Institución es pública o privada?'] == 'Pública'])}"),
            ]),
        ]
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)

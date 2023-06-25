import data
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# leer los dataframe de las licenciaturas, maestrias y doctorados
df_lic = data.df_lic
df_master = data.df_master
df_doc = data.df_doc
df = data.df

# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}
estados = data.estados_dict

# se cran las tarjetas que contendran la informacion mas relevante
# first_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H5("Card title", className="card-title"),
#             html.P("This card has some text content, but not much else"),
#             dbc.Button("Go somewhere", color="primary"),
#         ]
#     )
# )


# second_card = dbc.Card(
#     dbc.CardBody(
#         [
#             html.H5("Card title", className="card-title"),
#             html.P(
#                 "This card also has some text content and not much else, but "
#                 "it is twice as wide as the first card."
#             ),
#             dbc.Button("Go somewhere", color="primary"),
#         ]
#     )
# )

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[
    # dbc.themes.BOOTSTRAP,
    'style.css',
    # dbc.themes.SOLAR
    # dbc.themes.FLATLY
    # dbc.themes.QUARTZ
    # dbc.themes.VAPOR
    dbc.themes.CYBORG
]
)

# Definir el layout de la aplicació
app.layout = dbc.Container(
    [
        html.H1("Mapa de Programas Educativos"),
        dbc.Row(
            [
                # Columna de las tarjetas y el menú desplegable
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                html.Div(className="dropdown", children=[
                                    dbc.Label("Selecciona un Estado"),
                                    dcc.Dropdown(
                                        style={'background-color': '#696969',
                                               'color': 'black', 'border-radius': 20},
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
                            class_name="dark_tab",
                        ),
                        # dbc.Row(
                        #     [
                        #         dbc.Col(first_card, width=6),
                        #         dbc.Col(second_card, width=6),
                        #     ],
                        #     className="mb-3",
                        # ),
                        dbc.Row(
                            [
                                dbc.Col(id="stats"),
                            ]
                        ),
                    ],
                    # Ajustar el ancho de la columna
                    width={'size': 12, 'order': 'first'},
                    lg={'size': 4, 'order': 'first'}
                ),
                # Columna de las pestañas y el gráfico
                dbc.Col(
                    [
                        dcc.Tabs(id='tabs',
                                 value='tab-1',
                                 className='underTabs',
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
                        dcc.Graph(className="mapa",
                                  figure={}, id='maps', style={'border-radius': '20px !important',
                                                               'box-shadow': '0px 4px 4px rgba(0, 0, 0, 0.25)', 'margin': '0px', 'background-color': 'transparent'},
                                  config={
                                      'displayModeBar': False})
                    ],
                    # Adjust the width of the column
                    className='colMapa',
                    width={'size': 12, 'order': 'last'},
                    lg={'size': 8, 'order': 'last'},
                ),
            ],
            justify="between",
            align="center",
        ),
        # crear otra fila con columnas
        dbc.Row(
            [
                dbc.Col(id="general-stats"),
                # dbc.Col(id="sunburst-chart"),
            ]
        ),

    ],
    fluid=True,
)

# Callback para actualizar las opciones del menú desplegable de los estados


@app.callback(
    Output('estado', 'options'),
    [Input('tabs', 'value')]
)
def update_dropdown_options(tab):
    '''
    Actualiza las opciones del menú desplegable de los estados en función de la pestaña seleccionada.
    Args:
        tab (str): Pestaña seleccionada en la aplicación Dash.
    Returns:
        list: Listado de opciones para el menú desplegable de los estados.
        Cada opción es un diccionario con una etiqueta ("label") y un valor ("value").
    '''
    if tab == 'tab-1':
        df = df_lic
    elif tab == 'tab-2':
        df = df_master
    else:
        df = df_doc

    entidad_options = [{'label': entidad, 'value': entidad}
                       for entidad in df['Entidad Federativa donde se imparte'].unique()]

    return entidad_options

# Callback para renderizar el contenido del gráfico


@app.callback(
    Output('maps', 'figure'),
    [
        Input('tabs', 'value'),
        Input('estado', 'value')
    ],
)
def render_content(tab, estado):
    '''
    Genera una figura interactiva de dispersión en un mapa según la pestaña y estado seleccionados.
    Args:
        tab (str): Pestaña seleccionada en la aplicación Dash.
        estado (str): Estado seleccionado en el menú desplegable.
    Returns:
        plotly.graph_objects.Figure: Figura interactiva de dispersión en un mapa.
    '''
    hover_template = """
                        <b>Institución/Universidad:</b> %{customdata[0]}<br>
                        <b>Nombre del programa: </b> %{customdata[1]}<br>
                        <b>¿Pertenece al PNPC?:</b> %{customdata[2]}<br>
                        <b>Dirección física:</b> %{customdata[3]}<br>
                        <b>Correo:</b> %{customdata[4]}<br>
                        <b>Sede:</b> %{customdata[5]}<br>
                        <b>Página web del programa:</b> <a href="%{customdata[6]}" target="_blank">%{customdata[6]}</a><br>
                    """
    if tab == 'tab-1':
        df = df_lic
        df_lic['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=800,
                                center={"lat": 23.6345, "lon": -102.5528},
                                size=df["size"],
                                color_discrete_sequence=["green"]
                                )
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre de la Carrera (Licenciatura)", "¿Pertenece al PNPC?", "Dirección física (Licenciatura)", "Correo", "Sede (Licenciatura)", "Página web del programa de Licenciatura (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="black",
            bordercolor="black"
        ))
    elif tab == 'tab-2':
        df = df_master
        df_master['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=800,
                                center={"lat": 23.6345, "lon": -102.5528},
                                size=df_master["size"],
                                color_discrete_sequence=["orange"])
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre del Programa (Maestría)", "¿Pertenece al PNPC? (Maestría)", "Dirección física (Maestría)", "Correo", "Sede (Maestría)", "Página web del programa de Maestría (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="black",
            bordercolor="black"
        ))
    else:
        df = df_doc
        df_doc['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=800,
                                center={"lat": 23.6345, "lon": -102.5528},
                                color_discrete_sequence=["red"],
                                size=df_doc["size"])
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre del programa de Doctorado", "¿Pertenece al PNPC? (Doctorado)", "Dirección física (Doctorado)", "Correo", "Sede (Doctorado)", "Página web del programa de Doctorado (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            font_color="black",
            bordercolor="black"
        ))

    zoom_levels = {
        'Aguascalientes': 12,
        'Baja California': 8,
        'Baja California Sur': 8,
        'Campeche': 8,
        'Chiapas': 8,
        'Chihuahua': 8,
        'Ciudad de México': 10,
        'Coahuila': 8,
        'Colima': 9,
        'Durango': 8,
        'Guanajuato': 9,
        'Guerrero': 8,
        'Hidalgo': 9,
        'Jalisco': 8,
        'Estado de México': 12,
        'Michoacán': 8,
        'Morelos': 10,
        'Nayarit': 9,
        'Nuevo León': 9,
        'Oaxaca': 8,
        'Puebla': 9,
        'Querétaro': 10,
        'Quintana Roo': 9,
        'San Luis Potosí': 9,
        'Sinaloa': 8,
        'Sonora': 8,
        'Tabasco': 9,
        'Tamaulipas': 6.5,
        'Tlaxcala': 11,
        'Veracruz': 8,
        'Yucatán': 9,
        'Zacatecas': 9,
    }

    if estado is not None:
        df_estado = df[df['Entidad Federativa donde se imparte'] == estado]

        if len(df_estado) > 0:
            zoom_level = zoom_levels.get(estado, 8)

            fig.update_mapboxes(
                domain={'x': [0, 1], 'y': [0, 1]},
                center=dict(lat=df_estado['lat'].mean(),
                            lon=df_estado['lon'].mean()),
                zoom=zoom_level,
                style='open-street-map',
                bearing=0
            )

            fig.update_layout(
                mapbox_center={"lat": float(df_estado['lat'].mean()),
                               "lon": float(df_estado['lon'].mean())}
            )
            # fig.update_layout(mapbox_zoom=6)
            # fig.update_mapboxes(
            #     zoom=8,
            #     style='open-street-map',
            #     center=dict(lat=df_estado['lat'].mean(),
            #                 lon=df_estado['lon'].mean())
            # )
            # fig.update_layout(
            #     mapbox={
            #         'center': {'lat': df_estado['lat'].mean(), 'lon': df_estado['lon'].mean()},
            #         'zoom': 8,
            #         'style': 'open-street-map'
            #     }
            # )
        else:
            fig.update_layout(
                mapbox_center={"lat": 23.6345, "lon": -102.5528}
            )
            fig.update_layout(mapbox_zoom=4.2,
                              )
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
            },
            tittle_text='Programas de Doctorado en México'
        )

        fig.update_layout(
            mapbox=dict(
                # style='carto-darkmatter',  # Set the mapbox style to a desired theme
                layers=[],  # Remove any default layers
            ),
            # Set the plot background color to transparent
            plot_bgcolor='rgba(0,0,0,0)',
            # Set the paper background color to transparent
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),  # Set the margin to 0
        )

    return fig

# Callback para actualizar las estadísticas al seleccionar cada TAB


@app.callback(
    Output('stats', 'children'),
    [
        Input('tabs', 'value'),
        Input('estado', 'value')]
)
def update_stats(tab, estado):
    '''
    Esta función se encarga de actualizar las estadísticas de la entidad federativa seleccionada
    y las coloca en las tarjetas correspondientes.
    '''
    cards = []  # Lista para almacenar las tarjetas

    if estado is not None:
        if tab == 'tab-1':
            df_estado = df_lic[df_lic['Entidad Federativa donde se imparte'] == estado]
        elif tab == 'tab-2':
            df_estado = df_master[df_master['Entidad Federativa donde se imparte'] == estado]
        elif tab == 'tab-3':
            df_estado = df_doc[df_doc['Entidad Federativa donde se imparte'] == estado]

        # Verificar si la columna '¿La Institución es pública o privada?' existe en el DataFrame
        if '¿La Institución es pública o privada?' in df_estado.columns:
            total_publicas = len(
                df_estado[df_estado['¿La Institución es pública o privada?'] == 'Pública'])
            total_privadas = len(
                df_estado[df_estado['¿La Institución es pública o privada?'] == 'Privada'])

            # Crear tarjetas para las instituciones públicas y privadas
            cards.append(
                dbc.Card(
                    [
                        dbc.CardHeader(f"Para el estado de {estado}:"),
                        dbc.CardBody(
                            [
                                html.H4("Total de Instituciones Públicas:",
                                        className="card-title"),
                                html.H5(f"\t{total_publicas}",
                                        className="card-text"),
                            ]
                        ),
                    ],
                    className="card border-secondary mb-3",
                )
            )
            cards.append(
                dbc.Card(
                    [
                        dbc.CardHeader(f"Para el estado de {estado}:"),
                        dbc.CardBody(
                            [
                                html.H4("Total de Instituciones Privadas:",
                                        className="card-title"),
                                html.H5(f"\t{total_privadas}",
                                        className="card-text"),
                            ]
                        ),
                    ],
                    className="card border-secondary mb-3",
                )
            )

        # Verificar si la columna '¿Pertenece al PNPC? (Maestría)' existe en el DataFrame
        if '¿Pertenece al PNPC? (Maestría)' in df_estado.columns or '¿Pertenece al PNPC? (Doctorado)' in df_estado.columns:
            if '¿Pertenece al PNPC? (Doctorado)' in df_estado.columns:
                total_pnpc = len(
                    df_estado[df_estado['¿Pertenece al PNPC? (Doctorado)'].isin(['Sí', 'Si'])])
            elif '¿Pertenece al PNPC? (Maestría)' in df_estado.columns:
                total_pnpc = len(
                    df_estado[df_estado['¿Pertenece al PNPC? (Maestría)'].isin(['Sí', 'Si'])])
            else:
                total_pnpc = 0

            # Crear tarjeta para las instituciones pertenecientes al PNPC
            cards.append(
                dbc.Card(
                    [
                        dbc.CardHeader(f"Para el estado de {estado}:"),
                        dbc.CardBody(
                            [
                                html.H4(
                                    "Total de Instituciones pertenecientes al PNPC:", className="card-title"),
                                html.H5(f"\t{total_pnpc}",
                                        className="card-text"),
                            ]
                        ),
                    ],
                    className="card border-secondary mb-3",
                )
            )

    return cards

# Callback para actualizar las estadísticas generales y los gráficos de totales
@app.callback(
    Output('general-stats', 'children'),
    [Input('tabs', 'value')]
)
def update_general_stats(tab):
    '''
    Esta función se encarga de actualizar las estadísticas generales del dataframe
    y generar gráficos de algunos totales.
    '''
    cards = []  # Lista para almacenar las tarjetas
    total_pnpc = 0
    # Obtener los totales generales según la pestaña seleccionada
    if tab == 'tab-1':
        total_programs = len(df_lic)
        total_pnpc = len(df_lic[df_lic['¿Pertenece al PNPC?'] != 'No aplica'])
    elif tab == 'tab-2':
        total_programs = len(df_master)
        total_pnpc = len(
            df_master[df_master['¿Pertenece al PNPC? (Maestría)'].isin(["Si", "Sí"])])
    elif tab == 'tab-3':
        total_programs = len(df_doc)
        total_pnpc = len(
            df_doc[df_doc['¿Pertenece al PNPC? (Doctorado)'] == 'Si'])
    else:
        total_programs = 0
        total_pnpc = 0

    # Crear tarjetas para las estadísticas generales
    cards.append(
        dbc.Card(
            [
                dbc.CardHeader("Estadísticas Generales por nivel edicativo"),
                dbc.CardBody(
                    [
                        html.H4("Total de Programas:", className="card-title"),
                        html.H5(f"\t{total_programs}", className="card-text"),
                    ]
                ),
            ],
            className="card border-secondary mb-3",
        )
    )
    cards.append(
        dbc.Card(
            [
                dbc.CardHeader("Estadísticas Generales por nivel edicativo"),
                dbc.CardBody(
                    [
                        html.H4("Total de Programas PNPC:",
                                className="card-title"),
                        html.H5(f"\t{total_pnpc}", className="card-text"),
                    ]
                ),
            ],
            className="card border-secondary mb-3",
        )
    )

    # Generar gráfico de totales por tipo de programa
    df_totals = pd.DataFrame({
        'Tipo de Programa': ['Licenciatura', 'Maestría', 'Doctorado'],
        'Total': [len(df_lic), len(df_master), len(df_doc)]
    })

    fig = px.bar(df_totals, x='Tipo de Programa', y='Total', color='Tipo de Programa',
                 labels={'Total': 'Total de Programas', 'Tipo de Programa': 'Tipo de Programa'})
    fig.update_layout(title_text='Totales por Tipo de Programa')
    graph = dcc.Graph(figure=fig)

    cards.append(
        dbc.Card(
            [
                dbc.CardHeader("Gráfico de Totales por Tipo de Programa"),
                dbc.CardBody(graph),
            ],
            className="card border-secondary mb-3",
        )
    )

    df_lic["Nivel educativo"]= 'Licenciatura'
    df_master["Nivel educativo"] = "Maestría"
    df_doc["Nivel educativo"] = 'Doctorado'

    df_count_lic = df_lic.groupby(['Nivel educativo', 'Entidad Federativa donde se imparte']).size().reset_index(name='Total')
    df_count_master = df_master.groupby(['Nivel educativo','Entidad Federativa donde se imparte']).size().reset_index(name='Total')
    df_count_doc = df_doc.groupby(['Nivel educativo','Entidad Federativa donde se imparte']).size().reset_index(name='Total')
    df_combined = pd.concat([df_count_lic, df_count_master, df_count_doc], ignore_index=True)
    
    fig_sunburst = px.sunburst(df_combined, path=['Nivel educativo', 'Entidad Federativa donde se imparte'], values='Total') 

    cards.append(
        dbc.Card(
            [
                dbc.CardHeader("Gráfico de Sunburst por Nivel Educativo y Estado"),
                dbc.CardBody(dcc.Graph(figure=fig_sunburst)),
            ],
            className="card border-secondary mb-3",
        )
    )

    return cards


if __name__ == '__main__':
    app.run_server(debug=True, port=5000)

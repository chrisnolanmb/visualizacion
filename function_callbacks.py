import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from data import *


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
    <b>Nombre del programa:</b> %{customdata[1]}<br>
    <b>¿Pertenece al PNPC?:</b> %{customdata[2]}<br>
    <b>Dirección física:</b> %{customdata[3]}<br>
    <b>Correo:</b> %{customdata[4]}<br>
    <b>Sede:</b> %{customdata[5]}<br>
    <b>Página web del programa:</b> <a href="%{customdata[6]}" target="_blank" style="color:white; font-weight:bold;">%{customdata[6]}</a><br>
    """
    if tab == 'tab-1':
        df = df_lic
        df_lic['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=700,
                                center={"lat": 23.6345, "lon": -102.5528},
                                size=df["size"],
                                color_discrete_sequence=["#00667C"]
                                )
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre de la Carrera (Licenciatura)", "¿Pertenece al PNPC?", "Dirección física (Licenciatura)", "Correo", "Sede (Licenciatura)", "Página web del programa de Licenciatura (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="rgba( 36, 36, 36, 0.65)",
            font_size=16,
            font_family="Raleway",
            font_color="white",
            bordercolor="rgba( 36, 36, 36, 0.65 )"
        ), margin=dict(l=0, r=0, t=0, b=0))
    elif tab == 'tab-2':
        df = df_master
        df_master['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=700,
                                center={"lat": 23.6345, "lon": -102.5528},
                                size=df_master["size"],
                                color_discrete_sequence=["#E85D7E"])
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre del Programa (Maestría)", "¿Pertenece al PNPC? (Maestría)", "Dirección física (Maestría)", "Correo", "Sede (Maestría)", "Página web del programa de Maestría (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="rgba( 36, 36, 36, 0.65)",
            font_size=16,
            font_family="Raleway",
            font_color="white",
            bordercolor="rgba( 36, 36, 36, 0.65 )"
        ), margin=dict(l=0, r=0, t=0, b=0))
    else:
        df = df_doc
        df_doc['size'] = 10
        fig = px.scatter_mapbox(df,
                                lat=df["lat"],
                                lon=df.lon,
                                zoom=4.7,
                                height=700,
                                center={"lat": 23.6345, "lon": -102.5528},
                                color_discrete_sequence=["#7D5CB8"],
                                size=df_doc["size"])
        fig.update_traces(customdata=df[["Institución/Universidad", "Nombre del programa de Doctorado", "¿Pertenece al PNPC? (Doctorado)", "Dirección física (Doctorado)", "Correo", "Sede (Doctorado)", "Página web del programa de Doctorado (si hubiera)"]],
                          hovertemplate=hover_template)
        fig.update_layout(hoverlabel=dict(
            bgcolor="rgba( 36, 36, 36, 0.65)",
            font_size=16,
            font_family="Raleway",
            font_color="white",
            bordercolor="rgba( 36, 36, 36, 0.65 )"
        ), margin=dict(l=0, r=0, t=0, b=0))

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
        'Hidalgo': 11,
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
        'Sonora': 7.5,
        'Tabasco': 9,
        'Tamaulipas': 6.5,
        'Tlaxcala': 11,
        'Veracruz': 7.5,
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
        )
        fig.update_layout(
            mapbox=dict(
                layers=[],  # Remove any default layers
            ),
            # Set the plot background color to transparent
            plot_bgcolor='rgba(0,0,0,0)',
            # Set the paper background color to transparent
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),  # Set the margin to 0
        )

    return fig


def update_stats(tab, estado):
    '''
    Esta función se encarga de actualizar las estadísticas de la entidad federativa seleccionada
    y las coloca en las tarjetas correspondientes.
    '''
    cards = []  # Lista para almacenar las tarjetas
    if estado == "vacio":
        if tab == 'tab-1':
            total_programs = len(df_lic)
            total_pnpc = len(
                df_lic[df_lic['¿Pertenece al PNPC?'] != 'No aplica'])
            max_area = conteo_areas_lic[conteo_areas_lic['Frecuencia'] ==
                                        conteo_areas_lic['Frecuencia'].max()]['Área'].iloc[0]
            max_area_freq = conteo_areas_lic['Frecuencia'].max()
        elif tab == 'tab-2':
            total_programs = len(df_master)
            total_pnpc = len(
                df_master[df_master['¿Pertenece al PNPC? (Maestría)'].isin(["Si", "Sí"])])
            max_area = conteo_areas_master[conteo_areas_master['Frecuencia']
                                           == conteo_areas_master['Frecuencia'].max()]['Área'].iloc[0]
            max_area_freq = conteo_areas_master['Frecuencia'].max()
        elif tab == 'tab-3':
            total_programs = len(df_doc)
            total_pnpc = len(
                df_doc[df_doc['¿Pertenece al PNPC? (Doctorado)'] == 'Si'])
            max_area = conteo_areas_doc[conteo_areas_doc['Frecuencia'] ==
                                        conteo_areas_doc['Frecuencia'].max()]['Área'].iloc[0]
            max_area_freq = conteo_areas_doc['Frecuencia'].max()
        else:
            total_programs = 0
            total_pnpc = 0
            max_area = "No aplica"
            max_area_freq = 0

        # Crear tarjetas para las estadísticas generales
        cards.append(
            dbc.Col(
                [
                    dbc.Card(
                        [
                            dbc.CardHeader("Por nivel educativo"),
                            dbc.CardBody(
                                [
                                    html.H4("Total de Programas:",
                                            className="card-title"),
                                    html.H5(f"\t{total_programs}",
                                            className="card-text"),
                                ]
                            ),
                        ],
                        className="card border-secondary mb-3 shadow",
                    ),
                    dbc.Card(
                        [
                            dbc.CardHeader("Por nivel educativo"),
                            dbc.CardBody(
                                [
                                    html.H4("Total de Programas PNPC:",
                                            className="card-title"),
                                    html.H5(f"\t{total_pnpc}",
                                            className="card-text"),
                                ]
                            ),
                        ],
                        className="card border-secondary mb-3",
                    ),
                    # Crear tarjeta para el área de interés mayor
                    cards.append(
                        dbc.Card(
                            [
                                dbc.CardHeader("Área de interés mayor"),
                                dbc.CardBody(
                                    [
                                        html.H5(f"\t{max_area}",
                                                className="card-text"),
                                        html.H4("Frecuencia:",
                                                className="card-title"),
                                        html.H5(f"\t{max_area_freq}",
                                                className="card-text"),
                                    ]
                                ),
                            ],
                            className="card border-secondary mb-3 shadow",
                        )
                    )
                ],
            )
        )
    if estado != "vacio":
        if tab == 'tab-1':
            df_estado = df_lic[df_lic['Entidad Federativa donde se imparte'] == estado]
            # Obtener el área de interés mayor y su frecuencia para Licenciatura en el estado seleccionado
            # max_area_freq = conteo_areas_lic_estado[(conteo_areas_lic_estado['Área(s) de interés (Doctorado)'] == max_area) & (conteo_areas_lic_estado['Entidad Federativa donde se imparte'] == estado)]['Frecuencia'].iloc[0]
        elif tab == 'tab-2':
            df_estado = df_master[df_master['Entidad Federativa donde se imparte'] == estado]
            # Obtener el área de interés mayor y su frecuencia para Licenciatura en el estado seleccionado
            # max_area_freq = conteo_areas_master_estado[(conteo_areas_master_estado['Área'] == max_area) & (conteo_areas_master_estado['Entidad Federativa donde se imparte'] == estado)]['Frecuencia'].iloc[0]
        elif tab == 'tab-3':
            df_estado = df_doc[df_doc['Entidad Federativa donde se imparte'] == estado]
            # Obtener el área de interés mayor y su frecuencia para Licenciatura en el estado seleccionado
            # max_area_freq = conteo_areas_doc_estado[(conteo_areas_doc_estado['Área'] == max_area) & (conteo_areas_doc_estado['Entidad Federativa donde se imparte'] == estado)]['Frecuencia'].iloc[0]

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
                                        className="c"),
                                html.H5(f"\t{total_publicas}",
                                        className="card-text"),
                            ]
                        ),
                    ],
                    className="card border-secondary mb-3 shadow",
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
                    className="card border-secondary mb-3 shadow",
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
                    className="card border-secondary mb-3 shadow",
                )
            )

    return cards


def update_general_stats(tab):
    '''
    Esta función se encarga de actualizar las estadísticas generales del dataframe
    y generar gráficos de algunos totales.
    '''
    cards = []  # Lista para almacenar las tarjetas
    total_pnpc = 0
    # Generar gráfico de totales por tipo de programa
    fig = px.bar(df_totals, x='Tipo de Programa', y='Total', color='Tipo de Programa',
                 labels={'Total': 'Total de Programas',
                         'Tipo de Programa': 'Tipo de Programa'},
                 color_discrete_sequence=[
                     "#00667C", "#E85D7E", "#7D5CB8"],
                 )
    fig.update_layout(
        plot_bgcolor='#242424',
        paper_bgcolor='#242424',
        modebar=dict(
            remove=True
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        legend_font=dict(
            size=16,
            color='white'
        ),
        font=dict(
            size=16,
            color='white'
        ),
        legend_entrywidth=50,

        legend_entrywidthmode='pixels',
        legend_itemwidth=40,
        legend_orientation='v'


    )
    graph = dcc.Graph(figure=fig)

    cards.append(
        dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader("Por nivel educativo"),
                        dbc.CardBody(graph),
                    ],
                    className="card border-secondary mb-3",
                )
                ], )
    )

    fig_sunburst = px.sunburst(df_combined, path=[
                               'Nivel educativo', 'Entidad Federativa donde se imparte', 'Institución/Universidad'], values='Total', color_discrete_sequence=[
        "#00667C", "#E85D7E", "#7D5CB8"])
    cards.append(
        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader(
                        "Gráfico de Sunburst por Nivel Educativo y Estado"),
                    dbc.CardBody(dcc.Graph(figure=fig_sunburst)),
                ],
                className="card border-secondary mb-3 shadow",
            )
        ]
        )

    )
    fig_sunburst.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(
            size=16,
            color='white'
        ),
        grid_columns=2,

    )

    # Generar el gráfico de barras agrupadas utilizando Plotly Express
    fig_areas = px.bar(df_conteo, x="Nivel", y="Frecuencia", color="Área", barmode="group",
                       hover_data=["Nivel", "Área", "Frecuencia"], title="Frecuencia de áreas de interés",
                       labels={"Frecuencia": "Frecuencia", "Nivel": "Nivel de estudio"})
    # Ocultar la leyenda
    fig_areas.update_layout(
        plot_bgcolor='#242424',
        paper_bgcolor='#242424',
        modebar=dict(
            remove=True
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        legend_font=dict(
            size=16,
            color='white'
        ),
        font=dict(
            size=16,
            color='white'
        ),
        legend_entrywidth=300,
        legend_itemsizing='trace',
        legend_entrywidthmode='pixels',
        legend_itemwidth=30,
        legend_orientation='h',
        legend_title_side='left',
        legend_valign='middle'

    )

    cards.append(
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    [
                        dbc.CardHeader(
                            "Gráfico de Áreas de Interés por Nivel Educativo"),
                        dbc.CardBody(dcc.Graph(figure=fig_areas)),
                    ],
                    className="card border-secondary mb-3 shadow",
                )
            ],
            )
        ]),


    )

    return cards

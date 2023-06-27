from data import *
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from function_callbacks import *


# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}
estados = estados_dict

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[
    'style.css',
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
                                html.Div(className="", children=[
                                    dbc.Label("Selecciona un Estado",
                                              style={'color': 'white', 'font-size': 28}),
                                    dcc.Dropdown(
                                        style={'background-color': '#696969',
                                               'color': 'black', 'border-radius': 5, 'border': '1px solid rgba(255, 255, 255, 0.18)'},
                                        id="estado",
                                        options=[
                                            {"label": col, "value": col} for col in estados
                                        ],
                                        value="vacio",
                                    ),
                                ],
                                ),
                            ],
                            body=True,
                            class_name="card-title shadow ",
                            style={
                                'border': '1px solid rgba(255, 255, 255, 0.18)'},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(id="stats"),
                            ]
                        ),
                    ],
                    # Ajustar el ancho de la columna
                    width={'size': 12, 'order': 'first'},
                    lg={'size': 4, 'order': 'first'},
                    className='primera-columna'
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
                                             selected_className='custom-tab--selected lic'
                                             ),
                                     dcc.Tab(label='Maestría',
                                             value='tab-2',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected mas'
                                             ),
                                     dcc.Tab(label='Doctorado',
                                             value='tab-3',
                                             className='custom-tab',
                                             selected_className='custom-tab--selected doc'
                                             )
                                 ]),
                        dcc.Graph(
                            figure={}, id='maps', style={'box-sizing': 'border-box', 'border-width': '1px',
                                                         'paper_bgcolor': 'rgba(0,0,0,0)',
                                                         'plot_bgcolor': 'rgba(0,0,0,0)'},
                            config={
                                'displayModeBar': False})
                    ],
                    # Adjust the width of the column
                    className='colMapa shadow',
                    width={'size': 12, 'order': 'last'},
                    lg={'size': 8, 'order': 'last'},
                ),
            ],
            justify="between",
            align="start",
            style={'margin-bottom': 30}
        ),
        # crear otra fila con columnas
        dbc.Row(
            [
                html.H2("Datos Generales"),
                dbc.Col(
                    id="general-stats",
                )
            ],


            className='datos-generales'

        ),

    ],
    fluid=True,
)

app.callback(
    Output('estado', 'options'),
    [Input('tabs', 'value')]
)(update_dropdown_options)


app.callback(
    Output('maps', 'figure'),
    [
        Input('tabs', 'value'),
        Input('estado', 'value')
    ],
)(render_content)


app.callback(
    Output('stats', 'children'),
    [
        Input('tabs', 'value'),
        Input('estado', 'value')]
)(update_stats)

app.callback(
    Output('general-stats', 'children'),
    [Input('tabs', 'value')]
)(update_general_stats)


# Iniciar el servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True)

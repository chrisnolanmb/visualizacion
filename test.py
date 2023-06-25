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
df = data.df

# Create a dictionary of all the map dataframes
df_dict = {'Licenciatura': df_lic, 'Maestría': df_master, 'Doctorado': df_doc}
estados = data.estados_dict


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

app.layout = html.Div(
    children=[
        html.Div(
            id="container",
            children=[
                html.H1("Mapa de Programas Educativos"),
                html.Div(
                    id="dropdown",
                    children=[
                        dcc.Dropdown(
                            options=[
                                {"label": "Opción 1", "value": "opcion1"},
                                {"label": "Opción 2", "value": "opcion2"},
                                {"label": "Opción 3", "value": "opcion3"},
                            ],
                            value="opcion1",
                        )
                    ],
                ),
                html.Div(
                    id="cards",
                    children=[
                        html.Div("Tarjeta 1"),
                        html.Div("Tarjeta 2"),
                        html.Div("Tarjeta 3"),
                        html.Div("Tarjeta 4"),
                        html.Div("Tarjeta 5"),
                    ],
                ),
                html.Div(id="map", children="Mapa"),
            ],
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

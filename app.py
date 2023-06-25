import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash import dcc

# Crear la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Crear un DataFrame de ejemplo
df = pd.DataFrame({'Estados': ['Texas', 'California', 'Florida']})

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1('Verificación de Estado'),
    dbc.Tabs([
        dbc.Tab(label='Tab 1', children=[
            dbc.Alert(id='alerta-tab-1', color='danger', dismissable=True, is_open=False),
            html.Br(),
            dcc.Dropdown(
                id='dropdown-estados-tab-1',
                options=[{'label': estado, 'value': estado} for estado in df['Estados']],
                value=None
            )
        ]),
        dbc.Tab(label='Tab 2', children=[
            dbc.Alert(id='alerta-tab-2', color='danger', dismissable=True, is_open=False),
            html.Br(),
            dcc.Dropdown(
                id='dropdown-estados-tab-2',
                options=[{'label': estado, 'value': estado} for estado in df['Estados']],
                value=None
            )
        ]),
        dbc.Tab(label='Tab 3', children=[
            dbc.Alert(id='alerta-tab-3', color='danger', dismissable=True, is_open=False),
            html.Br(),
            dcc.Dropdown(
                id='dropdown-estados-tab-3',
                options=[{'label': estado, 'value': estado} for estado in df['Estados']],
                value=None
            )
        ])
    ])
])

# Definir una función de devolución de llamada para verificar si el estado seleccionado existe en el DataFrame
@app.callback(
    dash.dependencies.Output('alerta-tab-1', 'is_open'),
    dash.dependencies.Output('alerta-tab-2', 'is_open'),
    dash.dependencies.Output('alerta-tab-3', 'is_open'),
    dash.dependencies.Input('dropdown-estados-tab-1', 'value'),
    dash.dependencies.Input('dropdown-estados-tab-2', 'value'),
    dash.dependencies.Input('dropdown-estados-tab-3', 'value')
)
def verificar_estado_seleccionado_tab(estado_tab_1, estado_tab_2, estado_tab_3):
    is_open_tab_1 = estado_tab_1 is not None and estado_tab_1 not in df['Estados']
    is_open_tab_2 = estado_tab_2 is not None and estado_tab_2 not in df['Estados']
    is_open_tab_3 = estado_tab_3 is not None and estado_tab_3 not in df['Estados']
    return is_open_tab_1, is_open_tab_2, is_open_tab_3

# Iniciar el servidor Dash
if __name__ == '__main__':
    app.run_server(debug=True)

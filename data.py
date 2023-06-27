import pandas as pd
import numpy as np
from unidecode import unidecode

# leyendo los datos
df = pd.read_csv("mapaComputacion.csv", sep=";", encoding='UTF-8')

# Crea un diccionario con los nombres de las columnas
new_names = {
    'correo': 'Correo',
    'Nombre_de_la_Carrera_(Licenciatura)': 'Nombre de la Carrera (Licenciatura)',
    'Institución/Universidad': 'Institución/Universidad',
    'Sede_(Licenciatura)': 'Sede (Licenciatura)',
    '¿Pertenece_al_PNPC?_(Maestría)': '¿Pertenece al PNPC? (Maestría)',
    'Página_web_del_programa_de_Licenciatura_(si_hubiera)': 'Página web del programa de Licenciatura (si hubiera)',
    'Entidad_Federativa_donde_se_imparte': 'Entidad Federativa donde se imparte',
    '¿Su_Institución_tiene_un_programa_Nivel_Licenciatura?': '¿Su Institución tiene un programa Nivel Licenciatura?',
    '¿Su_Institución_tiene_un_programa_Nivel_Maestría?': '¿Su Institución tiene un programa Nivel Maestría?',
    'Sede_(Maestría)': 'Sede (Maestría)',
    'Sede_(Doctorado)': 'Sede (Doctorado)',
    'Nombre_del_programa_de_Doctorado': 'Nombre del programa de Doctorado',
    'Página_web_del_programa_de_Doctorado_(si_hubiera)': 'Página web del programa de Doctorado (si hubiera)',
    '¿Su_Institución_tiene_un_programa_Nivel_Doctorado?': '¿Su Institución tiene un programa Nivel Doctorado?',
    'Nombre_del_Programa_(Maestría)': 'Nombre del Programa (Maestría)',
    'Dirección_física_(Licenciatura)': 'Dirección física (Licenciatura)',
    'Dirección_física_(Maestría)': 'Dirección física (Maestría)',
    'Dirección_física_(Doctorado)': 'Dirección física (Doctorado)',
    'Página_web_del_programa_de_Maestría_(si_hubiera)': 'Página web del programa de Maestría (si hubiera)',
    'Área(s)_de_interés_(Doctorado)': 'Área(s) de interés (Doctorado)',
    'Área(s)_de_interés_(Maestría)': 'Área(s) de interés (Maestría)',
    'Área(s)_de_interés_(Licenciatura)': 'Área(s) de interés (Licenciatura)',
    '¿La_Institución_es_pública_o_privada?': '¿La Institución es pública o privada?',
    '¿Pertenece_al_PNPC?_(Doctorado)': '¿Pertenece al PNPC? (Doctorado)',
    'mapaIframe': 'mapaIframe',
    'coordenadas': 'coordenadas',
    'lat': 'lat',
    'lon': 'lon'
}

# Renombra las columnas
df = df.rename(columns=new_names)
df[['lat', 'lon']] = df['coordenadas'].str.split(', ', expand=True)

# convertir las columnas "lon" y "lat" a tipo numérico
df['lon'] = pd.to_numeric(df['lon'])
df['lat'] = pd.to_numeric(df['lat'])


df.pop("mapaIframe")
df.pop("Marca_temporal")
# df = df.drop(['Marca_temporal',
#               '¿Su Institución tiene un programa Nivel Licenciatura?',
#               '¿Su Institución tiene un programa Nivel Maestría?',
#               '¿Su Institución tiene un programa Nivel Doctorado?',
#               'mapaIframe'], axis=1)

df = pd.DataFrame(df)
df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)

df.loc[24, 'lat'] = 19.4646508
df.loc[24, 'lon'] = -97.6871585


df.replace(" ", np.nan, inplace=True)
df.replace("na", np.nan, inplace=True)
df.fillna('No aplica', inplace=True)

# displayhook(df.head())
# Estados disponibles
# Lista de valores
estados = ['Estado de México', 'Puebla', 'Ciudad de México', 'Morelos', 'Hidalgo', 'Baja California', 'Michoacán', 'San Luis Potosí',
           'Tamaulipas', 'Veracruz', 'Colima', 'Sinaloa', 'Sonora', 'Tabasco', 'Zacatecas', 'Jalisco', 'Querétaro', 'Coahuila']
estados.sort()
# Crea un diccionario vacío
estados_dict = {}

# Recorre la lista y agrega cada valor al diccionario
for i, estado in enumerate(estados):
    estados_dict[estado] = i + 1


#### LICENCIATURA ####
df_lic = df.drop(["¿Pertenece al PNPC? (Maestría)",
                  "Sede (Maestría)",
                  "Sede (Doctorado)",
                  "Nombre del programa de Doctorado",
                  "Página web del programa de Doctorado (si hubiera)",
                  "Página web del programa de Doctorado (si hubiera)",
                  "Página web del programa de Doctorado (si hubiera)",
                  "Página web del programa de Maestría (si hubiera)",
                  "Área(s) de interés (Doctorado)",
                  "Área(s) de interés (Maestría)",
                  "¿Pertenece al PNPC? (Doctorado)",
                  "¿Pertenece al PNPC? (Doctorado)",
                  "Dirección física (Maestría)",
                  "Dirección física (Doctorado)",
                  "Nombre del Programa (Maestría)",
                  "coordenadas",
                  "¿Su Institución tiene un programa Nivel Maestría?",
                  "¿Su Institución tiene un programa Nivel Doctorado?"
                  ], axis=1)

df_lic = df_lic.drop([1, 3, 9, 22, 25, 27, 37, 35])
df_lic = df_lic.reset_index(drop=True)
df_lic['¿Pertenece al PNPC?'] = 'No aplica'

# df_lic


#### MAESTRIA ####
df_master = df.drop(["Nombre de la Carrera (Licenciatura)",
                     "Sede (Licenciatura)",
                     "Página web del programa de Licenciatura (si hubiera)",
                     "Sede (Doctorado)",
                     "Nombre del programa de Doctorado",
                     "Página web del programa de Doctorado (si hubiera)",
                     "Dirección física (Licenciatura)",
                     "Dirección física (Doctorado)",
                     "Área(s) de interés (Doctorado)",
                     "Área(s) de interés (Licenciatura)",
                     "¿Pertenece al PNPC? (Doctorado)",
                     "coordenadas",
                     "¿Su Institución tiene un programa Nivel Licenciatura?",
                     "¿Su Institución tiene un programa Nivel Doctorado?"
                     ], axis=1)
df_master = df_master.drop([0, 3, 9, 10, 11, 22, 23, 25, 31, 33, 36, 37, 38])
df_master = df_master.reset_index(drop=True)
# display(df_master)


#### DOCTORADO ####
df_doc = df.drop(["Nombre de la Carrera (Licenciatura)",
                  "¿Pertenece al PNPC? (Maestría)",
                  "Sede (Licenciatura)",
                  "Página web del programa de Licenciatura (si hubiera)",
                  "Sede (Maestría)",
                  "Nombre del Programa (Maestría)",
                  "Dirección física (Licenciatura)",
                  "Dirección física (Maestría)",
                  "Página web del programa de Maestría (si hubiera)",
                  "Área(s) de interés (Maestría)",
                  "Área(s) de interés (Licenciatura)",
                  "coordenadas",
                  "¿Su Institución tiene un programa Nivel Licenciatura?",
                  "¿Su Institución tiene un programa Nivel Maestría?"
                  ], axis=1)

df_doc = df_doc.drop([0, 2, 10, 11, 13, 14, 16, 23, 28,
                     29, 30, 31, 32, 33, 35, 36, 37])
df_doc = df_doc.reset_index(drop=True)
# df_doc

# Convertir el contenido del dataframe a mayúsculas y sin acentos
df_master['Área(s) de interés (Maestría)'] = df_master['Área(s) de interés (Maestría)'].apply(
    lambda x: unidecode(x.upper()))
df_lic['Área(s) de interés (Licenciatura)'] = df_lic['Área(s) de interés (Licenciatura)'].apply(
    lambda x: unidecode(x.upper()))
df_doc['Área(s) de interés (Doctorado)'] = df_doc['Área(s) de interés (Doctorado)'].apply(
    lambda x: unidecode(x.upper()))

# Obtener todas las áreas en una sola columna
areas_master = df_master['Área(s) de interés (Maestría)'].str.replace(
    ';', ',').str.split(',').explode().str.strip()
areas_lic = df_lic['Área(s) de interés (Licenciatura)'].str.replace(
    ';', ',').str.split(',').explode().str.strip()
areas_doc = df_doc['Área(s) de interés (Doctorado)'].str.replace(
    ';', ',').str.split(',').explode().str.strip()
# Contar la frecuencia de cada área
conteo_areas_master = areas_master.value_counts().reset_index()
conteo_areas_lic = areas_lic.value_counts().reset_index()
conteo_areas_doc = areas_doc.value_counts().reset_index()
# Renombrar las columnas del DataFrame de conteo
conteo_areas_master.columns = ['Área', 'Frecuencia']
conteo_areas_doc.columns = ['Área', 'Frecuencia']
conteo_areas_lic.columns = ['Área', 'Frecuencia']
# Combinar los dataframes en uno solo
df_conteo = pd.concat(
    [conteo_areas_master, conteo_areas_lic, conteo_areas_doc])

# Agregar una columna 'Nivel' para indicar la licenciatura, maestría o doctorado
df_conteo['Nivel'] = ['Maestría'] * len(conteo_areas_master) + ['Licenciatura'] * len(
    conteo_areas_lic) + ['Doctorado'] * len(conteo_areas_doc)


df_lic["Nivel educativo"] = 'Licenciatura'
df_master["Nivel educativo"] = "Maestría"
df_doc["Nivel educativo"] = 'Doctorado'

df_count_lic = df_lic.groupby(['Nivel educativo', 'Entidad Federativa donde se imparte',
                               'Institución/Universidad']).size().reset_index(name='Total')
df_count_master = df_master.groupby(
    ['Nivel educativo', 'Entidad Federativa donde se imparte', 'Institución/Universidad']).size().reset_index(name='Total')
df_count_doc = df_doc.groupby(['Nivel educativo', 'Entidad Federativa donde se imparte',
                               'Institución/Universidad']).size().reset_index(name='Total')

df_combined = pd.concat(
    [df_count_lic, df_count_master, df_count_doc], ignore_index=True)

df_totals = pd.DataFrame({
    'Tipo de Programa': ['Licenciatura', 'Maestría', 'Doctorado'],
    'Total': [len(df_lic), len(df_master), len(df_doc)]
})

max_area = df_conteo[df_conteo['Frecuencia'] ==
                         df_conteo['Frecuencia'].max()]['Área'].iloc[0]
max_area_freq = df_conteo['Frecuencia'].max()
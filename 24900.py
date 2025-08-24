# La tabla 24900 del Instituto Nacional de Estadística (INE) de España proporciona una descripción detallada del gasto de los hogares españoles. 
# Se basa en la Encuesta de Presupuestos Familiares y ofrece información sobre el gasto medio por hogar y por persona, así como su distribución.
# Esta tabla es fundamental para entender los patrones de consumo y la estructura del gasto en España, 
# permitiendo análisis económicos y sociales más profundos.
import requests
import pandas as pd
import json

# URL de la API del INE para la tabla 24900
# Tabla 24900 contiene datos sobre el gasto de los hogares españoles.
url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24900"

# Realizar la petición
response = requests.get(url)

# Verificar si la respuesta fue exitosa
if response.status_code == 200:
    # Cargar los datos en formato JSON
    data = response.json()
    print("Datos recibidos correctamente.") 
else:
    print(f"Error al acceder a la API: {response.status_code}")

print(data[0].keys())
print(data[0])

# Mostrar los primeros elementos con formato.
print(json.dumps(data, indent=2, ensure_ascii=False)) # Solo los dos primeros elementos para evitar un volcado muy grande.

# Usar json-normalize para convertir los datos anidados en un DataFrame
df = pd.json_normalize(data, record_path=['Data'], meta=['Nombre'])
print(df.head())

# Poner el campo 'Nombre' como índice
df['Nombre'] = df['Nombre'].str.replace('Base 2006. Anual.', '').str.strip()
df.set_index('Nombre', inplace=True)
# Mostrar las primeras filas del DataFrame
print(df.head())

# Procesar los datos para obtener un DataFrame legible
# Dividir el campo 'Nombre' en varias columnas
df['Nombre'] = df.index
#df[['indice', 'dato', 'tipo_dato', 'descripcion', 'quintil']] = df['Nombre'].str.split('.', expand=True)
# ...existing code...
df[['indice', 'dato', 'tipo_dato', 'descripcion', 'quintil']] = df['Nombre'].str.split('.', n=4, expand=True)
# Limpiar los valores de 'quintil' para eliminar puntos al final y reemplazar valores vacíos por None
df['quintil'] = df['quintil'].str.strip('.').replace('', None)

# ...existing code...
# Eliminar la columna 'Nombre' original
df.drop(columns=['Nombre'], inplace=True)
# Reordenar las columnas
df = df[['indice', 'dato', 'tipo_dato', 'descripcion', 'quintil', 'Anyo', 'Valor', 'Secreto']]
# Renombrar las columnas
df.rename(columns={'Anyo': 'anyo', 'Valor': 'valor', 'Secreto': 'secreto'}, inplace=True)
                   
# Muestra las primeras filas
print(df.head())

# Ver los distintos valores de las columnas
print("Valores únicos en 'indice':", df['indice'].unique())
print("Valores únicos en 'dato':", df['dato'].unique())
print("Valores únicos en 'tipo_dato':", df['tipo_dato'].unique())
print("Valores únicos en 'descripcion':", df['descripcion'].unique())   
print("Valores únicos en 'quintil':", df['quintil'].unique())

#######################################
# Guarda el DataFrame en un CSV
df.to_csv('datos_ine_24900_legible_new.csv', index=False)

# Mostrar información del DataFrame
print(df.info())
# Mostrar estadísticas descriptivas del DataFrame
#print(df.describe())
# Mostrar las columnas del DataFrame
print(df.columns)
# Mostrar el número de filas y columnas del DataFrame
print(f"Número de filas: {df.shape[0]}, Número de columnas: {df.shape[1]}")
# Mostrar los tipos de datos de las columnas    
print(df.dtypes)

# Comprobar que la suma de descripcion = "Distribución (porcentajes verticales)" para el año 2022 es 100%
df['valor'] = pd.to_numeric(df['valor'], errors='coerce')  # Asegurarse de que los valores son numéricos
df['anyo'] = pd.to_numeric(df['anyo'], errors='coerce')  # Asegurarse de que los años son numéricos
df_2022 = df[df['anyo'] == 2022]
# Quitar de la suma dato = "Índice general"
df_2022 = df_2022[df_2022['dato'] != 'Índice general']
# Imprimir df_2022 para verificar
print(df_2022)
# Filtrar por el quintil = "Total"
df_2022 = df_2022[df_2022['quintil'] == 'Total']
# Imprimir df_2022 para verificar
print(df_2022)
# Filtrar por la descripción "Distribución (porcentajes verticales)"
df_2022 = df_2022[df_2022['descripcion'] == 'Distribución (porcentajes verticales)']
# Imprimir df_2022 para verificar
print(df_2022)

# Calcular la suma de la columna 'valor'
suma_valores_2022 = df_2022['valor'].sum()
print(f"Suma de valores para el año 2022: {suma_valores_2022}")

# Comprobar si la suma es 100%
if suma_valores_2022 == 100:
    print("La suma de la descripción 'Distribución (porcentajes verticales)' para el año 2022 es 100%.")
else:
    print("La suma de la descripción 'Distribución (porcentajes verticales)' para el año 2022 NO es 100%.")

import requests
import pandas as pd
import json

def obtener_datos_ine(url):
    """Solicita los datos de la API del INE y devuelve el JSON."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al acceder a la API: {e}")
        return None

def procesar_datos(data):
    """Convierte los datos JSON en un DataFrame legible."""
    if not data:
        return None
    df = pd.json_normalize(data, record_path=['Data'], meta=['Nombre'])
    df['Nombre'] = df['Nombre'].str.replace('Base 2006. Anual.', '').str.strip()
    df.set_index('Nombre', inplace=True)
    df['Nombre'] = df.index
    df[['indice', 'dato', 'tipo_dato', 'descripcion', 'quintil']] = df['Nombre'].str.split('.', n=4, expand=True)
    df['quintil'] = df['quintil'].str.strip('.').replace('', None)
    df.drop(columns=['Nombre'], inplace=True)
    df = df[['indice', 'dato', 'tipo_dato', 'descripcion', 'quintil', 'Anyo', 'Valor', 'Secreto']]
    df.rename(columns={'Anyo': 'anyo', 'Valor': 'valor', 'Secreto': 'secreto'}, inplace=True)
    return df

def mostrar_info(df):
    """Muestra información relevante del DataFrame."""
    print(df.head())
    print(df.info())
    print(df.columns)
    print(f"Número de filas: {df.shape[0]}, Número de columnas: {df.shape[1]}")
    print(df.dtypes)
    print("Valores únicos en 'indice':", df['indice'].unique())
    print("Valores únicos en 'dato':", df['dato'].unique())
    print("Valores únicos en 'tipo_dato':", df['tipo_dato'].unique())
    print("Valores únicos en 'descripcion':", df['descripcion'].unique())
    print("Valores únicos en 'quintil':", df['quintil'].unique())

def main():
    url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/24900"
    data = obtener_datos_ine(url)
    if data:
        print("Datos recibidos correctamente.")
        print(f"Tipo de dato recibido: {type(data)}")
        print(f"Número de elementos en la lista: {len(data)}")
        print(data[0].keys())
        print(json.dumps(data[:2], indent=2, ensure_ascii=False))  # Solo los dos primeros elementos
        df = procesar_datos(data)
        if df is not None:
            mostrar_info(df)
            df.to_csv('datos_ine_tabla_24900_legible.csv', index=False)
            print("Datos guardados en 'datos_ine_tabla_24900_legible.csv'")
        else:
            print("No se pudo procesar el DataFrame.")
    else:
        print("No se recibieron datos.")

if __name__ == "__main__":
    main()
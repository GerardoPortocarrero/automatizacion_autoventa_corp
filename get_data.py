import pandas as pd
from datetime import datetime

# Conservar las filas que contenga las siguientes Locaciones
def get_relevant_locations(corp, LOCACIONES):
    corp = corp[corp['Locación'].isin(LOCACIONES)]
    return corp

# Eliminar todas las columnas excepto las relevantes
def get_relevant_columns(corp):
    corp = corp[['Locación', 'Día', 'Texto Breve de Producto', 'Volumen CF']]
    return corp

# Eliminar columna y fila vacia y asignar el encabezado
def adjust_excel_data(df):
    # Eliminar columnas unnamed (vacias)
    df = df.dropna(axis=1, how='all')

    # Tomar la fila 1 como nombres de columnas
    df.columns = df.iloc[1]
    
    # Eliminar las dos primeras filas (la original de encabezado y la fila de nombres)
    df = df.iloc[2:].reset_index(drop=True)

    # Convertir la fecha a string, incluso si los valores son datetime dentro de "object"
    df['Día'] = df['Día'].apply(lambda x: x.strftime('%d/%m/%Y') if isinstance(x, pd.Timestamp) or isinstance(x, datetime) else str(x))
    
    return df

def main(file_properties, LOCACIONES):
    df_corp = pd.read_excel(file_properties['name'], sheet_name=file_properties['sheet_name'], header=None)

    df_corp = adjust_excel_data(df_corp)

    df_corp = get_relevant_columns(df_corp)

    df_corp = get_relevant_locations(df_corp, LOCACIONES)

    return df_corp
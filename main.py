#!/usr/bin/env python
# coding: utf-8

# In[10]:


import pandas as pd
import numpy as np
import importlib
import time
import os
import warnings
warnings.filterwarnings("ignore")  # Oculta todos los warnings

# Mis modulos
import get_data as gd


# In[11]:


# import pyfiglet
# print(pyfiglet.figlet_format("Autoventa CORP"))

banner = r"""
    _         _                       _           ____ ___  ____  ____  
   / \  _   _| |_ _____   _____ _ __ | |_ __ _   / ___/ _ \|  _ \|  _ \ 
  / _ \| | | | __/ _ \ \ / / _ \ '_ \| __/ _` | | |  | | | | |_) | |_) |
 / ___ \ |_| | || (_) \ V /  __/ | | | || (_| | | |__| |_| |  _ <|  __/ 
/_/   \_\__,_|\__\___/ \_/ \___|_| |_|\__\__,_|  \____\___/|_| \_\_|                                                                          

          💥 AUTOMATIZADOR DE FORMATO AUTOVENTA CORPORATIVO 💥
"""

print(banner, end='\n\n')
time.sleep(1)


# In[12]:


# Variables de configuracion
PROJECT_ADDRESS = os.getcwd()

# Diccionarios
FILE_PROPERTIES = {
    'name': os.path.join(PROJECT_ADDRESS, 'query.xlsx'),
    'sheet_name': 'AutovtaSUR',
}
tablas_por_locacion = {} # Guardar los DataFrames por Locacion

# Listas
LOCACIONES = ['06 AYA EL PEDREGAL', '40 AYA CHALA', '88 AYA CAMANA']


# In[15]:


importlib.reload(gd)

df_corp = gd.main(FILE_PROPERTIES, LOCACIONES)
print(df_corp.info())


# In[16]:


# Obtener FECHAS y PRODUCTOS
FECHAS = sorted(df_corp["Día"].unique())
PRODUCTOS = df_corp["Texto Breve de Producto"].unique()


# In[ ]:


# Agrupar por Locacion
for locacion in df_corp["Locación"].unique():
    df_loc = df_corp[df_corp["Locación"] == locacion]

    # Pivotear para que las FECHAS sean columnas
    tabla = df_loc.pivot_table(
        index="Texto Breve de Producto",
        columns=df_loc["Día"],
        values="Volumen CF",
        aggfunc="sum",
        fill_value=0
    )

    # Asegurar que estén todas las FECHAS y PRODUCTOS (incluso si no hubo volumen)
    tabla = tabla.reindex(index=PRODUCTOS, columns=FECHAS, fill_value=0)

    # ❌ Elimina las filas donde el producto no tenga volumen en ninguna fecha
    tabla = tabla.loc[~(tabla == 0).all(axis=1)]

    tablas_por_locacion[locacion] = tabla


# In[ ]:


# Guardar las tablas por separado con separador ;
with open(os.path.join(PROJECT_ADDRESS, "query.csv"), "w", encoding="utf-8-sig", newline='') as f:
    for loc, tabla in tablas_por_locacion.items():
        f.write(f"{loc}\n")  # Escribe el nombre de la locación
        tabla_reset = tabla.reset_index()
        tabla_reset.to_csv(f, index=False, sep=";")  # <--- separador punto y coma
        f.write("\n")


# ### Export it as .py

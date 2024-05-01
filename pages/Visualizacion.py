import streamlit as st
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Configurar las credenciales y autorizar el cliente de Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Cargar las credenciales desde una variable de entorno
credentials_json = os.getenv('GOOGLE_CREDENTIALS')  # Asegúrate de que la variable de entorno esté bien configurada
credenciales_dict = json.loads(credentials_json) if credentials_json else None
credenciales = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_dict, scope)

cliente = gspread.authorize(credenciales)

# Obtener los datos de la hoja de cálculo
hoja_calculo = cliente.open("Base de datos 1").get_worksheet(0)
datos = hoja_calculo.get_all_values()

# Crear el DataFrame
df = pd.DataFrame(datos[1:], columns=datos[0])

# Mostrar los datos en una tabla usando Streamlit
st.write("Datos de la hoja de cálculo:")
st.write(df)

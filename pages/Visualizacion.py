import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar las credenciales y autorizar el cliente de Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_name("credential.json", scope)
cliente = gspread.authorize(credenciales)

# Obtener los datos de la hoja de cálculo
hoja_calculo = cliente.open("Base de datos 1").get_worksheet(0)
datos = hoja_calculo.get_all_values()

# Crear el DataFrame
df = pd.DataFrame(datos[1:], columns=datos[0])

# Mostrar los datos en una tabla usando Streamlit
st.write("Datos de la hoja de cálculo:")
st.write(df)

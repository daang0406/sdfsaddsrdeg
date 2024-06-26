import streamlit as st
from PIL import Image
import pandas as pd
from datetime import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="Solicitud de compra"
)

# Configuración de warnings
import warnings
warnings.filterwarnings('ignore')

# Conexión a Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_name("credential.json", scope)
cliente = gspread.authorize(credenciales)
Info = cliente.open("Base de datos 1").get_worksheet(0)

# Establecer la zona horaria
tz = pytz.timezone('America/Bogota')  # Ajusta esto a tu zona horaria

# Obtener fecha y hora actual ajustada a la zona horaria
fecha_actual = datetime.now(tz).date().strftime('%d/%m/%Y')
hora_actual = datetime.now(tz).time().strftime('%H:%M')

# Interfaz de usuario
st.title(f"Solicitud de compra {fecha_actual}")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

cantidad = st.number_input("Cantidad:", min_value=0, step=1)
montoUnidad = st.number_input("Monto por unidad:", min_value=0.0)
montoTotal = cantidad*montoUnidad
montoTotal_formateado = f"S/{montoTotal:.2f}"  
st.write("Monto total: ", montoTotal_formateado)
fecha = st.date_input("Fecha:", value=datetime.now(tz).date())
hora = st.write("Hora:", datetime.now(tz).time().strftime('%H:%M'))
descripcion = st.text_input("Descripción:")
estado = "Pendiente"

# Validación y envío de datos
if st.button("Enviar", key="Boton_enviar"):
    if descripcion and montoTotal and montoUnidad:
        data = [[descripcion, montoUnidad, montoTotal, cantidad, fecha.strftime('%d/%m/%Y'), hora_actual, estado]]
        columns = ['Descripción', 'Monto por unidad', 'Monto Total', 'Cantidad', 'Fecha', 'Hora', 'Estado']
        df = pd.DataFrame(data, columns=columns)
        sheet = cliente.open("Base de datos 1").get_worksheet(0)
        sheet.append_rows(df.values.tolist())
        st.success("¡Datos enviados exitosamente a Google Sheets!")
    else:
        st.warning("Por favor, llene todos los campos correspondientes antes de enviar.")

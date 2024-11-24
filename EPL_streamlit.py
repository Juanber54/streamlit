import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import random
from skimage import io

Logo = io.imread("./Imagenes/EPLlogo.png")
st.image(Logo, width = 500)

st.title("Premier League 23/24")
st.subheader(":violet[Análisis estadístico de diferentes parámetros ofensivos.]")

#Menú de configuración
st.sidebar.image(Logo, width = 200)
st.sidebar.markdown("## MENÚ DE CONFIGURACIÓN")

players = pd.read_csv('./Datos/EPL_df.csv')
st.markdown(":blue[**DATAFRAME PARA EL ANÁLISIS DE LA MEJOR LIGA DEL MUNDO**]")

st.markdown(":blue[Este DataFrame contiene información sobre las estadísticas de 240 jugadores de la EPL 23/24]")
st.markdown(":blue[Sin embargo, se debe resaltar que la base de datos puede tener cierto sesgo, "
"pues falta un porcentaje importante de los jugadores totales que estuvieron registrados durante esa temporada.]")
st.markdown(":blue[Esto se debe principalmente a varios jugadores no registraron prácticamente ningún dato "
"en los parámetros ofensivos que estamos considerando en este análisis]")

st.dataframe(players)
st.divider()

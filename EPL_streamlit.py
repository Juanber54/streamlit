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

#Gráfica 2 y 3
vars_team1 = ['Arsenal','Liverpool','Aston Villa','Fulham','Newcastle United','Brentford','Tottenham Hotspur','Nottingham Forest','Manchester United','West Ham United','Wolverhampton Wanderers','Chelsea','Luton Town','Manchester City','Brighton and Hove Albion','Burnley','Everton','Crystal Palace','Bournemouth','Sheffield United']
default_team1 = vars_team1.index('Liverpool')
team1_selected = st.sidebar.selectbox('Elección del Equipo 1 para el Gráfico:', vars_team1, index = default_team1)

vars_team2 = ['Arsenal.','Liverpool.','Aston Villa.','Fulham.','Newcastle United.','Brentford.','Tottenham Hotspur.','Nottingham Forest.','Manchester United.','West Ham United.','Wolverhampton Wanderers.','Chelsea.','Luton Town.','Manchester City.','Brighton and Hove Albion.','Burnley.','Everton.','Crystal Palace.','Bournemouth.','Sheffield United.']
default_team2 = vars_team2.index('Liverpool.')
team2_selected = st.sidebar.selectbox('Elección del Equipo 2 para el Gráfico:', vars_team2, index = default_team2)
st.sidebar.divider()

#Gráfica 4
vars_top = st.sidebar.slider('Cantidad de jugadores mostrados: ', 1, 9)
st.sidebar.divider()

#Gráfica 4 y 11
vars_stat = ['Shots per 90','Shot Conversion Rate (%)','Minutes','Matches','Expected Goals per 90','Goals per 90','Goals','Shots on Target per 90','Shot Accuracy (%)','90s','Total Shots','Total Shots on Target','Expected Goals']
default_stat = vars_stat.index('Goals')
stat_selected = st.sidebar.selectbox('Elección de los Parámetros para el Gráfico:', vars_stat, index = default_stat)
st.sidebar.divider()

#Gráfica 11
selec_val_corr = st.sidebar.radio("Valores de Correlación:", options = ['Activo', 'Inactivo'])
if selec_val_corr == 'Activo':
    anotacion = True
elif selec_val_corr == 'Inactivo':
    anotacion = False

#Gráfica 11
stat_multi_selected = st.sidebar.multiselect('Parámetros de la Matriz de Correlación:', vars_stat, default = vars_stat)

#Gráfica 11
vars_cmap = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges',
             'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn',
             'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter',
             'cool', 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
             'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv',
             'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
             'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
             'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral', 'gist_ncar']
color_selected = st.sidebar.selectbox('Paleta de Color para la Matriz de Correlación:', vars_cmap)
if st.sidebar.button('Color Aleatorio') == True:
    color_selected = random.choice(vars_cmap)

#PANEL CENTRAL
players = pd.read_csv('./Datos/EPL_df.csv')
st.markdown("**DATAFRAME PARA EL ANÁLISIS DE LA MEJOR LIGA DEL MUNDO**")

st.markdown(":blue[Este DataFrame contiene información sobre las estadísticas de 240 jugadores de la EPL 23/24.]")
st.markdown(":blue[Sin embargo, se debe resaltar que la base de datos puede tener cierto sesgo, "
"pues falta un porcentaje importante de los jugadores totales que estuvieron registrados durante esa temporada.]")
st.markdown(":blue[Esto se debe principalmente a que varios jugadores no registraron prácticamente ningún dato "
"en los parámetros ofensivos que estamos considerando en este análisis.]")

st.dataframe(players)
st.divider()

#Gráfica 1
st.subheader('Jugadores por Equipo')
fig1, ax1 = plt.subplots()
plt.rcParams.update({'font.size': 8, 'figure.figsize': (8, 8)}) 
players.groupby('Team').size().plot(kind='pie', explode=[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
                                                           , 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
                                                           , 0.01, 0.01, 0.01, 0.01], autopct='%.2f%%', cmap='tab10')
st.pyplot(fig1)

#Gráfica 2
jug_pais = players[['Country','Team']]
jug_p_pais = jug_pais.groupby(['Team','Country']).value_counts()
jug_pais_df = pd.DataFrame(jug_p_pais)
st.subheader('Nacionalidades por Equipo')
fig2, ax1 = plt.subplots()
sns.set_style('darkgrid')
sns.histplot(data=jug_pais_df, x='Team', palette='twilight')
plt.xticks(rotation=90)
st.pyplot(fig2)

#Gráfica 3 y 4
st.subheader('Comparación estadísticas ofensivas')
colum_izq, colum_der = st.columns(2)
colum_izq.markdown(team1_selected)
fig3, ax1 = plt.subplots()
análisis_ofensivo = players[['Team','Total Shots','Total Shots on Target','Goals','Expected Goals']]
análisis_ofensivo = pd.DataFrame(análisis_ofensivo.groupby(['Team']).sum())
equipo1 = análisis_ofensivo.loc[team1_selected]
equipo1 = equipo1.transpose()
equipo1 = equipo1.to_frame()
equipo1 = equipo1.rename(columns={1: 'Parámetro'})
sns.countplot(x=equipo1, color='lightblue', edgecolor='black')
ax1.set_xlabel(team1_selected)
ax1.set_ylabel('Valor')
colum_izq.pyplot(fig3)

colum_der.markdown(team2_selected)
fig4, ax2 = plt.subplots()
equipo2 = análisis_ofensivo.loc[team2_selected]
equipo2 = equipo2.transpose()
equipo2 = equipo2.to_frame()
equipo2 = equipo2.rename(columns={1: 'Parámetro'})
sns.countplot(x=equipo2, color='red', edgecolor='black')
ax2.set_xlabel(team2_selected)
ax2.set_ylabel('Valor')
colum_der.pyplot(fig4)

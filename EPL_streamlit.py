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

# Subheader para la comparación
st.subheader('Comparación de estadísticas ofensivas')
colum_izq, colum_der = st.columns(2)
#estadisticas_ofensivas = ['Total Shots on Target', 'Goals', 'Expected Goals']
estadisticas_ofensivas = stat_multi_selected
análisis_ofensivo_df = players.groupby('Team')[estadisticas_ofensivas].sum()

# Gráfica 3 (primer equipo)
colum_izq.markdown(f"**Equipo seleccionado:** {team1_selected}")
equipo1 = análisis_ofensivo_df.loc[team1_selected].to_frame(name='Valor')
equipo1['Estadística'] = equipo1.index
fig3, ax1 = plt.subplots()
sns.barplot(data=equipo1, x='Estadística', y='Valor', palette='mako', ax=ax1)
ax1.set_title(team1_selected)
ax1.set_xlabel('Categoría')
ax1.set_ylabel('Valores')
colum_izq.pyplot(fig3)

# Gráfica 4 (segundo equipo)
team2_select = team2_selected[:len(team2_selected)-1]
colum_der.markdown(f"**Equipo seleccionado:** {team2_select}")
equipo2 = análisis_ofensivo_df.loc[team2_select].to_frame(name='Valor')
equipo2['Estadística'] = equipo2.index
fig4, ax2 = plt.subplots()
sns.barplot(data=equipo2, x='Estadística', y='Valor', palette='rocket', ax=ax2)
ax2.set_title(team2_select)
ax2.set_xlabel('Categoría')
ax2.set_ylabel('Valores')
colum_der.pyplot(fig4)

#Gráfica 5
st.subheader('Líderes estadísticos')
top_goles = pd.DataFrame(players[stat_selected])
top_goles = top_goles.sort_values(by=stat_selected[0], ascending=False)
top_goles_lim = top_goles.iloc[:top_selected+1]
fig5, ax1 = plt.subplots()
sns.countplot(x=top_goles_lim, color='lightblue', edgecolor='black')
st.pyplot(fig5)

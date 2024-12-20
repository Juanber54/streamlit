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
team1_selected = st.sidebar.selectbox('Elección del Equipo 1:', vars_team1, index = default_team1)

vars_team2 = ['Arsenal.','Liverpool.','Aston Villa.','Fulham.','Newcastle United.','Brentford.','Tottenham Hotspur.','Nottingham Forest.','Manchester United.','West Ham United.','Wolverhampton Wanderers.','Chelsea.','Luton Town.','Manchester City.','Brighton and Hove Albion.','Burnley.','Everton.','Crystal Palace.','Bournemouth.','Sheffield United.']
default_team2 = vars_team2.index('Liverpool.')
team2_selected = st.sidebar.selectbox('Elección del Equipo 2:', vars_team2, index = default_team2)
st.sidebar.divider()

#Gráfica 4
vars_top = st.sidebar.slider('Cantidad de jugadores mostrados: ', 1, 10)
st.sidebar.divider()

#Gráfica 4 y 11
vars_stat = ['Shots per 90','Shot Conversion Rate (%)','Minutes','Matches','Expected Goals per 90','Goals per 90','Goals','Shots on Target per 90','Shot Accuracy (%)','90s','Total Shots','Total Shots on Target','Expected Goals']
default_stat = vars_stat.index('Goals')
stat_selected = st.sidebar.selectbox('Parámetro líderes estadísticos:', vars_stat, index = default_stat)
st.sidebar.divider()

#Gráfica 11
stat_multi_selected = st.sidebar.multiselect('Parámetros para Gráficos:', vars_stat, default = vars_stat)
st.sidebar.divider()

#Gráfica 11
selec_val_corr = st.sidebar.radio("Valores de Correlación:", options = ['Activo', 'Inactivo'])
if selec_val_corr == 'Activo':
    anotacion = True
elif selec_val_corr == 'Inactivo':
    anotacion = False

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
st.divider()

#Gráfica 2
jug_pais = players[['Country','Team']]
jug_p_pais = jug_pais.groupby(['Team','Country']).value_counts()
jug_pais_df = pd.DataFrame(jug_p_pais)
st.subheader('Variedad de Nacionalidades por Equipo')
fig2, ax1 = plt.subplots(figsize=(6, 3))
sns.set_style('darkgrid')
sns.histplot(data=jug_pais_df, x='Team', palette='twilight')
plt.xticks(rotation=90)
st.pyplot(fig2)
st.divider()

st.subheader('Comparación de estadísticas ofensivas')
colum_izq, colum_der = st.columns(2)
estadisticas_ofensivas = stat_multi_selected
análisis_ofensivo_df = players.groupby('Team')[estadisticas_ofensivas].sum()

# Gráfica 3 (primer equipo)
colum_izq.markdown(f"**Equipo seleccionado:** {team1_selected}")
equipo1 = análisis_ofensivo_df.loc[team1_selected].to_frame(name='Valor')
equipo1['Estadística'] = equipo1.index
fig3, ax1 = plt.subplots(figsize=(4,3))
sns.barplot(data=equipo1, x='Estadística', y='Valor', palette='mako', ax=ax1)
ax1.set_xlabel('Categoría', fontsize=10)
ax1.set_ylabel('Valores', fontsize=10)
colum_izq.pyplot(fig3)

# Gráfica 4 (segundo equipo)
team2_select = team2_selected[:len(team2_selected)-1]
colum_der.markdown(f"**Equipo seleccionado:** {team2_select}")
equipo2 = análisis_ofensivo_df.loc[team2_select].to_frame(name='Valor')
equipo2['Estadística'] = equipo2.index
fig4, ax2 = plt.subplots(figsize=(4,3))
sns.barplot(data=equipo2, x='Estadística', y='Valor', palette='rocket', ax=ax2)
ax2.set_xlabel('Categoría', fontsize=10)
ax2.set_ylabel('Valores', fontsize=10)
colum_der.pyplot(fig4)

#Gráfica 5
st.divider()
st.subheader('Líderes estadísticos')
top_goles = players[['Player', stat_selected]].copy()
top_goles = top_goles.sort_values(by=stat_selected, ascending=False).head(vars_top)
fig5, ax1 = plt.subplots(figsize=(10, 7))
sns.barplot(data=top_goles, x=stat_selected, y='Player', palette='viridis', ax=ax1)
ax1.set_title(f'Top {vars_top} jugadores en {stat_selected}', fontsize=14)
ax1.set_xlabel(stat_selected, fontsize=12)
ax1.set_ylabel('Jugador', fontsize=12)
st.pyplot(fig5)
st.divider()

#Gráfica 6
st.subheader('Aprovechamiento de oportunidades de cara a gol')
goles_equipos = players[['Team', 'Goals','Expected Goals']]
top_goles_equipos = pd.DataFrame(goles_equipos.groupby(['Team']).sum())
fig6, ax1 = plt.subplots(figsize=(7, 5))
plt.plot(top_goles_equipos['Goals'],   color = 'green',   label = 'Goals', linewidth=2)
plt.plot(top_goles_equipos['Expected Goals'],   color = 'blue',   label = 'Expected Goals', linewidth=2)
plt.title('Goals and Expected Goals per Team')
plt.legend(loc='best')
plt.xlabel('Equipo')
plt.ylabel('Valores')
plt.xticks(rotation=85)
st.pyplot(fig6)
st.divider()

#Gráfica 7
st.subheader('Correlación tiros a puerta vs goles/goles esperados')
colum_izq, colum_der = st.columns(2)
with colum_izq:
    fig7, ax1 = plt.subplots(figsize=(5, 4))
    players.plot(kind='scatter', x='Shots on Target per 90', y='Goals per 90', color='green', ax=ax1)
    plt.title('Disparos a puerta vs Goles')
    plt.xlabel('Shots on Target per 90')
    plt.ylabel('Goals per 90')
    st.pyplot(fig7)

#Gráfica 8
with colum_der:
    fig8, ax2 = plt.subplots(figsize=(5, 4))
    players.plot(kind='scatter', x='Shots on Target per 90', y='Expected Goals per 90', color='blue',ax=ax2)
    plt.title('Disparos a puerta vs Goles esperados')
    plt.xlabel('Shots on Target per 90')
    plt.ylabel('Expected Goals per 90')
    st.pyplot(fig8)

st.divider()
st.subheader('Otras correlaciones')

# Gráfica 9
fig9, ax1 = plt.subplots(figsize=(8, 7))
ax1.scatter(players['Shot Accuracy (%)'], players['Goals'], color='purple', alpha=0.7)
ax1.set_title('Shot Accuracy vs Goals scored', fontsize=12)
ax1.set_xlabel('Shot Accuracy (%)', fontsize=10)
ax1.set_ylabel('Goals scored', fontsize=10)
st.pyplot(fig9)

# Gráfica 10
fig10, ax2 = plt.subplots(figsize=(8, 7))
ax2.scatter(players['Minutes'], players['Goals'], color='grey', alpha=0.7)
ax2.set_title('Minutes played vs Goals scored', fontsize=12)
ax2.set_xlabel('Minutes played', fontsize=10)
ax2.set_ylabel('Goals scored', fontsize=10)
st.pyplot(fig10)
st.divider()

#Gráfica 11
st.subheader('Matriz de Correlación')
fig11, ax1 = plt.subplots(figsize=(6, 5))
df_corr = players[stat_multi_selected].corr()
sns.heatmap(df_corr, annot = anotacion, fmt='.2f', cmap = color_selected)
st.pyplot(fig11)

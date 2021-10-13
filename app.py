#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import plotly.express as px
import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import folium_static
from PIL import Image


# In[2]:


#Dashboard titel en breedte
st.set_page_config(layout="wide")
st.title('Dashboard Elektrische Voertuigen Nederland')
img = Image.open("foto.png")
st.image(img, width=800)
'....'


# In[3]:


#Sidebar info
st.sidebar.subheader('Gemaakt Door:')
st.sidebar.write('• Mara van Boeckel')
st.sidebar.write('• Aniska Sinnige')
st.sidebar.write('• Maarten van der Veer')
st.sidebar.write('• Mark Yonan')


# In[4]:


st.header('Map Visualisaties')
st.markdown('#')
st.subheader('Aantal Laadpalen Drenthe')
'...'


# In[5]:


#Code laadpalen Drenthe
gpd_provinces = gpd.read_file('provinces.geojson')
df_map = pd.read_csv('map_data_cleaned.csv')
df_dr = df_map[df_map['Province'] == 'Drenthe']

map_dr = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4)

for row in df_dr.iterrows():
    row_values = row[1] 
    location = [row_values['LAT'], row_values['LNG']]
    popup = ('Adres: ' + str(row_values['Address Line']))
    marker = folium.Marker(location = location, popup = popup, icon=folium.Icon(icon='flash', color='green'))
    marker.add_to(map_dr)
    
folium.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', 
                 attr='Mapbox attribution', name='Terrain').add_to(map_dr)
    
folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_dr)

folium_static(map_dr)


# In[6]:


st.markdown('#')
st.markdown('#')
st.subheader('Heatmap Laadpalen Drenthe')
'...'


# In[7]:


#Code heatmap Drenthe
map_heat = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4)

map_heat.add_child(plugins.HeatMap(df_dr[['LAT', 'LNG']].values, radius=19))
folium.Marker(location=[52.993668, 6.548259],popup='<strong>'+'Assen'+'</strong>').add_to(map_heat)
folium.Marker(location=[52.7558037, 6.9095851],popup='<strong>'+'Emmen'+'</strong>').add_to(map_heat)
folium.Marker(location=[52.7286158, 6.4701002],popup='<strong>'+'Hoogeveen'+'</strong>').add_to(map_heat)
folium.Marker(location=[53.1383574, 6.4123693],popup='<strong>'+'Roden'+'</strong>').add_to(map_heat)
folium.Marker(location=[53.0841274, 6.6648434],popup='<strong>'+'Zuidlaren'+'</strong>').add_to(map_heat)

folium.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', 
                 attr='Mapbox attribution', name='Terrain').add_to(map_heat)

folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_heat)

folium_static(map_heat)


# In[8]:


st.markdown('#')
st.markdown('#')
st.subheader('Tarieven Laadpalen Drenthe')
'...'


# In[9]:


#Code tarieven laadpalen
def bekend(prijs):
    if prijs != 0:
        color = 'green'
    elif prijs == 0:
        color = 'red'
        
    return color

#popup voor tarief
def prijs(totaal):
    if totaal != 0:
        popup = '€' + str(totaal) + ' per kWh'
    elif totaal == 0:
        popup = 'Onbekend Tarief'
        
    return popup


map_tr = folium.Map(location=[52.9476012, 6.6230586], zoom_start=9.4)

for row in df_dr.iterrows():
    row_values = row[1] 
    location = [row_values['LAT'], row_values['LNG']]
    popup = (prijs(row_values['Usage Cost']))
    marker = folium.Marker(location = location, popup = popup, icon=folium.Icon(icon='flash', 
                                                                                color=bekend(row_values['Usage Cost'])))
    marker.add_to(map_tr)
    
folium.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', 
                 attr='Mapbox attribution', name='Terrain').add_to(map_tr)
    
folium.GeoJson(gpd_provinces.iloc[0]['geometry']).add_to(map_tr)

folium_static(map_tr)


# In[10]:


st.markdown('#')
st.markdown('#')
st.subheader('Gemaakte Laadpalen per Jaar Nederland')
'...'


# In[11]:


#Code histogram laadpalen jaren
df_map['Date Created'] = pd.to_datetime(df_map['Date Created'])

fig = px.histogram(x=df_map['Date Created'].dt.year)

fig.update_layout({'xaxis':{'title':{'text': 'Jaar'}},
                   'yaxis':{'title':{'text':'Aantal Gemaakte Laadpalen'}},
                   'title':{'text':'Gemaakte laadpalen per jaar Nederland', 'x':0.5}}, 
                  xaxis = dict(tickmode = 'linear', tick0 = 2011, dtick = 1), 
                  bargap=0.2)    

st.plotly_chart(fig)


# In[12]:


st.markdown('#')
st.subheader('Aantal Laadpalen per Provincie')
'...'


# In[13]:


#Code laadpalen per provincie
df_lprov= pd.read_csv('Laadpaal_Prov.csv')
df_lprov_pivot = df_lprov.pivot(columns=['name'], values='# Laadpalen')
df_lprov_pivot.fillna(0, inplace=True)

fig1 = px.choropleth_mapbox(df_lprov, geojson=gpd_provinces, color='# Laadpalen', locations='name', 
                            center={"lat": 52.210216, "lon":4.895168 }, 
                            mapbox_style="carto-positron", zoom=6, featureidkey="properties.name", 
                            color_continuous_scale='reds')

fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

button1 =  dict(method = "update",
                args = [{'z': [ df_lprov['# Laadpalen'] ] }],
                label = "Alle")
button2 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Noord-Holland'] ]}],
                label = "Noord-Holland")
button3 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Zuid-Holland'] ]}],
                label = "Zuid-Holland")
button4 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Zeeland'] ]}],
                label = "Zeeland")
button5 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Noord-Brabant'] ]}],
                label = "Noord-Brabant")
button6 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Limburg'] ]}],
                label = "Limburg")
button7 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Utrecht'] ]}],
                label = "Utrecht")
button8 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Gelderland'] ]}],
                label = "Gelderland")
button9 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Overijssel'] ]}],
                label = "Overijssel")
button10 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Drenthe'] ]}],
                label = "Drenthe")
button11 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Groningen'] ]}],
                label = "Groningen")
button12 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Friesland (Fryslân)'] ]}],
                label = "Friesland")
button13 =  dict(method = "update",
                args = [{'z': [ df_lprov_pivot['Flevoland'] ]}],
                label = "Flevoland")

fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.update_layout(coloraxis_colorbar_thickness=23,
                  updatemenus=[dict(buttons=[button1, button2, button3, button4, button5, button6, button7, button8,
                                            button9, button10, button11, button12, button13])]) 

st.plotly_chart(fig1)


# In[14]:


st.markdown('#')
st.markdown('#')
st.markdown('#')
st.header('Laadpaal Visualisaties')
st.markdown('#')
st.subheader('Verdeling Laadtijden')
'...'


# In[15]:


#Code verdeling laadtijden
paal = pd.read_csv('laadpaaldata2.csv')

fig2 = px.histogram(paal, x='M2')

x=paal['M2'].mean()
x1=paal['M2'].median()
fig2.add_annotation(x=x, y=400, arrowhead=1, text='<b>Gemiddelde : 232 min</b>')
fig2.add_annotation(x=x1, y=1000, arrowhead=1, text='<b>Mediaan : 58 min</b>', xanchor='left')

fig2.update_layout({'xaxis':{'title':{'text': 'Laadtijd (min)'}},
                   'yaxis':{'title':{'text':'Frequentie'}}, 
                   'title':{'text':'Histogram van de laadtijd', 'x':0.5}})
fig2.update(layout_xaxis_range = [0,1024])
fig2.update_layout(bargap=0.2, xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 50))

st.plotly_chart(fig2)


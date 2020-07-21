import pandas as pd
from  sqlalchemy import create_engine
from geopy.geocoders import Nominatim
import json
import requests
import plotly.graph_objects as go

geolocator = Nominatim(user_agent='teste')

r = requests.get('https://brasil.io/api/dataset/covid19/caso_full/data/')
response = r.json()
df = pd.read_json(json.dumps(response))
     
parsed_dataframe = df.drop(axis=1, columns=['next', 'previous'], index=None)

cidades_latitude = []
cidades_longitude = []
cidades = []
ultimos_casos_confirmados = []

for result in parsed_dataframe['results']:
    if str(result['city']) != 'None':
        cidades.append(result['city'])
        cidades_geoinfos =  geolocator.geocode(dict(country='Brazil', city=result['city']), timeout=10)
        cidades_latitude.append(getattr(cidades_geoinfos, 'latitude', 'None'))
        cidades_longitude.append(getattr(cidades_geoinfos, 'longitude', 'None'))
        ultimos_casos_confirmados.append(result['last_available_confirmed'])

df = pd.DataFrame({'cidade': cidades,'latitude': cidades_latitude,'longitude': cidades_longitude,'ultimos_casos_confirmados': ultimos_casos_confirmados})
fig = go.Figure(data=go.Scattergeo(lon = df['longitude'], lat = df['latitude'], text = df['cidade'], mode = 'markers', marker_color = df['ultimos_casos_confirmados']))
fig.update_layout(title = 'Cidades com maior numero de casos confirmados', geo_scope='brazil')
fig.show()
import random
import os
import pycountry
import pandas as pd
import pickle
import redis
from geopy.geocoders import Nominatim
import plotly.graph_objects as go

quantidade = int(os.environ['QUANTIDADE'])

class Deus(object):
    def crie_pessoas(self):
        geolocator = Nominatim(user_agent='teste')  
        r = redis.StrictRedis(host='34.95.202.190',port=6379, db=0, password='SMCJ5agypTaN')
        paises_info = {}
        paises = []
        paises_latitude = []
        paises_longitude = []
        paises_count = []

        for i in range(1, quantidade):
            pais = random.choices(list(pycountry.countries))[0].name

            if r.exists(pais):
                pais_local = pickle.loads(r.get(pais))

            else:
                pais_local = geolocator.geocode(dict(country=pais), timeout=10)
                result = pickle.dumps(pais_local)
                r.set(pais, result)

            if pais in paises_info:
                paises_info[pais]['Count'] += 1
            
            else:
                paises_info[pais] = {'Latitude': getattr(pais_local, 'latitude', 'null'),
                    'Longitude': getattr(pais_local, 'longitude', 'null'),'Count': 1}   

        for k in paises_info.keys():
            paises.append(k)
            paises_latitude.append(paises_info[k]['Latitude'])
            paises_longitude.append(paises_info[k]['Longitude'])
            paises_count.append(paises_info[k]['Count'])

        df = pd.DataFrame({'pais': paises,'latitude': paises_latitude,'longitude': paises_longitude,'count': paises_count})

        fig = go.Figure(data=go.Scattergeo(lon = df['longitude'], lat = df['latitude'], text = df['pais'], mode = 'markers', marker_color = df['count'],))

        fig.update_layout(title = 'Nacionalidades entrevistadas durante o estudo.', geo_scope='world',)
        fig.show()

deus = Deus()
deus.crie_pessoas()
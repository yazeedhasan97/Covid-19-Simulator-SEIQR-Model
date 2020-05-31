import gmaps
import gmaps.datasets as gd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as implt


gmaps.configure(api_key='AIzaSyBqmaSMESUuaWht383WqtEtLDyGff5GrKs')

df_earth = gd.load_dataset_as_df('earthquakes')
print(df_earth.head())

locations = df_earth[['latitude', 'longitude']]
weights = df_earth['magnitude']


fig = gmaps.figure()
fig.add_layer(gmaps.heatmap_layer(locations))

fig
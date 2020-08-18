import folium
import itertools
import json
import requests
import pandas as pd
from find_trends import find_current_trends

def load_map_with_trends():

	find_current_trends()
	m = folium.Map(tiles='Stamen Terrain',  zoom_start=3, location=[20.76, 79])
	country_cordinates = pd.read_csv('trending_cities.csv')
	tooltip = 'See Trends'
	lat = country_cordinates['lat']
	lon = country_cordinates['lng']
	city = country_cordinates['city']
	for i, city in enumerate(city):
		try:
			folium.Marker([lat[i], lon[i]], popup = '<i>This is {}<i>'.format(city), tooltip = tooltip).add_to(m)
		except: pass
	m.save('templates/trends_on_the_map.html')

	return None

if __name__ == '__main__':

	load_map_with_trends()

import folium
import itertools
import json
import requests
import pandas as pd
from find_trends import find_current_trends
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def load_map_with_trends():

	find_current_trends()
	m = folium.Map(tiles='Stamen Terrain',  zoom_start=3, location=[20.76, 79])
	country_cordinates = pd.read_csv('trending_cities.csv')
	tooltip = 'See Trends'
	lat = country_cordinates['lat']
	lon = country_cordinates['lng']
	city = country_cordinates['city']
	trends = country_cordinates['trends']
	#print('Marking cities')
	for i, city in enumerate(city):
		try:
			folium.Marker([lat[i], lon[i]], popup = '<i>{}<i>'.format(trends[i]), tooltip = tooltip).add_to(m)
		except: pass
	m.save('templates/trends_on_the_map.html')

	return None

sched.start()
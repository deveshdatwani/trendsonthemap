from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=('GET','POST'))
def main_page():

	if request.method == 'GET':

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
	
		return	render_template('trends_on_the_map.html')

	return m._repr_html_()

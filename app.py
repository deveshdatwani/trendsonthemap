from flask import Flask, render_template, request
import pandas as pd
import mysql.connector
import folium

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=('GET','POST'))
def main_page():

	if request.method == 'GET':

		tooltip = 'See Trends'
	
		connector = mysql.connector.connect(user='be5852720363b4', password='936fcbd3', host='us-cdbr-east-02.cleardb.com', database='heroku_4ac3cade96b682b')
		m = folium.Map(tiles='Stamen Terrain',  zoom_start=3, location=[20.76, 79])

		if connector.is_connected():	
			cursor = connector.cursor()
			query = 'SELECT * FROM trendsincities'
			cursor.execute(query)
			response = cursor.fetchall()
			cursor.close()
			connector.close()

			for i, city in enumerate(response):
								
				folium.Marker([round(city[4],2), round(city[5],2)], popup = '<i>{}<i>'.format(city[6]), tooltip = tooltip).add_to(m)
				
	return m._repr_html_()

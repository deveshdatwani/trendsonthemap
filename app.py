from flask import Flask, render_template, request, url_for
import pandas as pd
import mysql.connector
import folium
from jinja2 import PackageLoader, select_autoescape, Environment, Template
from apscheduler.schedulers.background import BackgroundScheduler
from find_trends import find_trends

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

sched = BackgroundScheduler(daemon=True)
sched.add_job(find_trends, 'interval', minutes=5)
sched.start()

@app.route('/', methods=('GET','POST'))
def main_page():
    if request.method == 'GET':
        tooltip = 'See Trends'
        connector = mysql.connector.connect(user='devesh', password='trendsonthemap', host='localhost', database='trends')
        m = folium.Map(tiles='Stamen Terrain', min_zoom=3, zoom_start=3, location=[20.76, 79])
        folium.TileLayer(opacity=1).add_to(m)

    if connector.is_connected():
        cursor = connector.cursor()
        query = 'SELECT * FROM trendsincities'
        cursor.execute(query)
        response = cursor.fetchall()
        cursor.close()
        connector.close()

    for i, city in enumerate(response):
        try:            
            folium.Marker([round(city[4],2), round(city[5],2)], popup = '<i>><span style="font-weight:900; margin-left:30%;">{}</span><br><br>{}<i>'.format(city[1], '<br>'.join(city[6].split('-')[:10])), tooltip = tooltip).add_to(m)

        except Exception as e: print(e)

    final_display = m._repr_html_()

    env = Environment(loader=PackageLoader('app', 'templates'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('trends.html')
    map = template.render(map=final_display)

    return map


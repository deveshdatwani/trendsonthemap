# Trends On The Map

### The Webpage
https://www.trendsonthemap.com

## Webpage Snippet

![](https://github.com/deveshdatwani/trendsonthemap/blob/master/trends.PNG) 

## Introduction

Social media has seen exponential growth in the number of its users for about a decade now. More and more people turn to social media to voice their opnions or share parts of their life. Twitter has become a medium on which ideas, opinions and beliefs are shared.

In Twitter, a word, phrase or a hashtag mentioned by a large number of users in a short period of time is said to be "trending topic" or simply "trending" at that point of time. Twitter provides with a funtionality to retrieve the trending topics based on locations through its API.\

Trendsonthemap aims to visualize trends on a map allowing users to catch up with world trends without hastles.

![](https://github.com/deveshdatwani/trendsonthemap/blob/master/twitter-trends.PNG)

A GET request made with authentic API secret key credentials returns JSON file which contains trending topics and in some cases the number of tweets.

## Technologies Used

*Python
*HTML and CSS
*Folium
*Jinja2
*apschedular
*MYSQL

## Installation and Launch (Linux)

From the Terminal, clone the github repository with the command

```
git clone https://github.com/deveshdatwani/trendsonthemap
```

You will also need to set up a mysql server on your machine. Once that is done, import the trendsonthemap schema from the data directory into your msql-server. Do so by using the following command 

```
mysql -u username -p trendsonthemap < file.sql
```

trendsonthemap uses data from this database to access trends. Trends are updated every 90 minutes (more or less).

Then move into the folder with the command

```
cd trendsonthemap
```

After you have installed all the dependencies, you can launch the flask app with the "flask" command. Before that you need to tell Flask where to look for the app. Do this through the export command

```
export FLASK_APP=app.py
```

Then run flaskk app with the command 

```
flask run / python3 -m flask run
```

You will see an output similar to this:

![](https://github.com/deveshdatwani/trendsonthemap/blob/master/snippet3.png.png)

You can then visit the page at http://127.0.0.1:5000 to check out your webapp.

## Project Walkthrough

The two modules which run the webapp are app.py and find_trends.py. Whenever a call is made to '/' page of the server, the main_page function decorated by flask's app first connects to the database to fetch trends, latitude and longitude of every city. It then creates markers on the folium map.


Folium binds this into an html template which is then embedded in an iframe of another jinja template.


-- mysql-connector connecting to the database.

```
connector = mysql.connector.connect(user='devesh', password='trendsonthemap', host='localhost', database='trends')
		m = folium.Map(tiles='Stamen Terrain', min_zoom=3, zoom_start=3, location=[20.76, 79])

		if connector.is_connected():
			cursor = connector.cursor()
			query = 'SELECT * FROM trendsincities'
			cursor.execute(query)
			response = cursor.fetchall()
			cursor.close()
			connector.close()
```

-- folium creating a map and marking cities from the latitude and longitude values from database as well as the trends.

```
for i, city in enumerate(response):

				try:

					folium.Marker([round(city[4],2), round(city[5],2)], popup = '<i>><span style="font-weight:900; margin-left:30%;">{}</span><br><br>{}<i>'.format(city[1], '<br>'.join(city[6].split('-')[:10])), tooltip = tooltip).add_to(m)

				except Exception as e: print(e)

		final_display = m._repr_html_()
```

find_trends.py fetches city based trends from Twitter through its API and stores it in the database. Since Twitter allows only 70 requests a minute. An iterator has been set up in the database to fetch city based trends in a batch of 15 every 5 minutes. This is done using the apschedular tool.

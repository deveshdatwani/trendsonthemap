import os
from boto.s3.connection import S3Connection
import requests
import pandas as pd

#bearer_token = S3Connection(os.environ['BEARER_TOKEN'])

def find_current_trends():

	url = 'https://api.twitter.com/1.1/trends/available.json'
	bearer = os.environ['BEARER_TOKEN']
	response = requests.get(url=url, headers = {'authorization': 'Bearer ' + bearer})
	worldwide_trending = response.json()

	city_coordinates = pd.read_csv('worldcities.csv')
	trending_woeid = [[trend['name'], trend['country'], trend['woeid']] for trend in worldwide_trending]
	trending_woeid = pd.DataFrame(trending_woeid, columns = ['city', 'country', 'woeid'])

	city_coordinates = city_coordinates[['city', 'lat', 'lng', 'country']]
	trending_cities = trending_woeid.merge(city_coordinates, on=['country','city'])

	trending_cities.to_csv('trending_cities.csv')
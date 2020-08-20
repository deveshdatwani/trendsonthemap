import os
#from boto.s3.connection import S3Connection
import requests
import pandas as pd

def find_current_trends():

    bearer_token = os.environ['BEARER_TOKEN']
    with open('inter.txt', 'r') as f:
        inter = f.read()
        f.close()
    inter = int(inter)
    print('The txt file contains the number {}'.format(inter))
    split_end = int(inter) * 70
    print('split end = {}'.format(split_end))
    split_start = int(split_end) - 70
    print('split start = {}'.format(split_start))
    url = 'https://api.twitter.com/1.1/trends/available.json'
    bearer = os.environ['BEARER_TOKEN']
    response = requests.get(url=url, headers = {'authorization': 'Bearer ' + bearer})
    response = response.json()
    trending_cities = []
    print('Available trends acquired')

    for trend in response:
        trending_cities.append([trend['name'], trend['country'], trend['woeid']])

    print(trending_cities)
    trending_cities_df = pd.DataFrame(trending_cities, columns=['city','country','woeid'])
    city_coordinates = pd.read_csv('worldcities.csv')
    city_coordinates = city_coordinates[['city','country','lat','lng']]
    trending_cities_df = trending_cities_df.merge(city_coordinates,on=['country','city'])
    print(trending_cities_df)
    woeids = trending_cities_df['woeid'].values
    trends_in_woeids = []
    url2 = 'https://api.twitter.com/1.1/trends/place.json'
    woeids = woeids[split_start:split_end]

    for woeid in woeids:
        param = {'id':woeid}
        response = requests.get(url = url2, headers = {'authorization': 'Bearer ' + bearer}, params = param).json()
        print('Acquiring trends for {}'.format(woeid))
        trends_in_woeids.append(response)	
        #print(response)

    print('All trends acquired')
    trending_seventy_in_woeids = trends_in_woeids
    l1 = []
    print(len(trending_seventy_in_woeids))
    print(trending_seventy_in_woeids)

    for i in trending_seventy_in_woeids:
        l2 = []
        for j in i[0]['trends']:
            l2.append(j['name'])
        l1.append(l2)

    print(l1)
    trending_seventy = trending_cities_df[split_start:split_end]
    trending_seventy.insert(5, 'trends', l1)
    trending_seventy.to_csv('trending_cities.csv')

    if inter > 4:
        with open('inter.txt', 'w') as f:
            f.truncate(0)
            f.write('{}'.format('1'))
            f.close()
    else:
        inter += 1
        print(inter)
    with open('inter.txt', 'w') as f:
        f.truncate(0)
        f.write('{}'.format(str(inter)))
        f.close()
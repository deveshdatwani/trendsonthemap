import os
import requests
import pandas as pd
from time import sleep
import mysql.connector
from apscheduler.schedulers.blocking import BlockingScheduler

def find_trends():
    bearer = 'insert your bearer token from your Twitter API app'

    connector = mysql.connector.connect(user='devesh', password='trendsonthemap', host='localhost', database='trends')
    print('connected to database')

    if connector.is_connected():
        cursor = connector.cursor(buffered=True)
        query = 'SELECT * FROM iterator WHERE holder = "it_holder" '
        cursor.execute(query)
        response = cursor.fetchone()
    i = response[1]

    if i > 19:
        response = 1
    else:
        response = response[1] + 1

    print('Updated iterator {}'.format(response))
    second_query = "UPDATE iterator SET it = {} WHERE holder = 'it_holder' ".format(response)
    cursor.execute(second_query)
    connector.commit()
    third_query = 'SELECT * FROM trendsincities'
    third_response = cursor.execute(third_query)
    response = cursor.fetchall()
    print('iterator token accessed and updated. Fetched trendingcities')

    split_end = i * 20
    split_start = split_end - 20
    print('start and end {} - {}'.format(split_start, split_end))

    trends = [x[6] for x in response]
    woeids = [x[3] for x in response]
    woeids_copy = woeids
    trends_copy = trends
    woeids = list(woeids[split_start:split_end])
    trends = list(trends[split_start:split_end])
    trends_in_woeids = []
    url = 'https://api.twitter.com/1.1/trends/place.json'
    l2 = []
    response = []

    if len(woeids) > 0:

        for woeid in woeids:
            param = {'id' : woeid}
            r = requests.get(url = url, headers = {'authorization': 'Bearer ' + bearer}, params = param).json()
            response.append(r)

        for i in response:
            l1 = []
            print(i)
            for j in i[0]['trends']:
                l1.append(j['name'])
            l2.append('-'.join(l1))

        trends = l2
        trends = tuple(trends)
        cursor.close()
        connector.close()
        connector = mysql.connector.connect(user='devesh', password='trendsonthemap', host='localhost', database='trends')
        cursor = connector.cursor(buffered=True)

        for i, trend in enumerate(trends):
            cursor.execute('UPDATE trendsincities SET trends = %s WHERE woeid = %s', (trend, woeids[i]))
            print(trend)
            connector.commit()

        cursor.close()
        connector.close()

    else:
        pass

    return None

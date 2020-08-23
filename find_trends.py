import os
import requests
import pandas as pd
from time import sleep
import mysql.connector

def find_current_trends():

    bearer = os.environ['BEARER_TOKEN']
    print('trying to connect to server')
    connector = mysql.connector.connect(user='be5852720363b4', password='936fcbd3', host='us-cdbr-east-02.cleardb.com', database='heroku_4ac3cade96b682b')
    
    if connector.is_connected():    
        cursor = connector.cursor(buffered=True)
        query = 'SELECT * FROM iterator WHERE holder = "it_holder" '
        cursor.execute(query)
        response = cursor.fetchone()
        i = response[1]
        response = response[1] + 1
        print('This is update iterator {}'.format(response))
        second_query = "UPDATE iterator SET it = {} WHERE holder = 'it_holder' ".format(response)
        cursor.execute(second_query)
        connector.commit()
        third_query = 'SELECT * FROM trendsincities'
        third_response = cursor.execute(third_query)
        response = cursor.fetchall()
        print('iterator token accessed and updated. Fetched trendingcities')
        print(i)

    split_end = i * 5
    split_start = split_end - 5

    trends = [x[6] for x in response]
    woeids = [x[3] for x in response] 
    #print(woeids)
    woeids = woeids[split_start:split_end]
    trends_in_woeids = []
    url = 'https://api.twitter.com/1.1/trends/place.json'
    l2 = []

    for woeid in woeids:
        param = {'id' : woeid}
        response = requests.get(url = url, headers = {'authorization': 'Bearer ' + bearer}, params = param).json()
        l1 = []
        #print(response)
        for i in response[0]['trends']:
            l1.append(i['name'])
        l2.append(l1)

    print('All trends acquired')

    trends[split_start:split_end] = l2
    #print(trends)
    connector = mysql.connector.connect(user='be5852720363b4', password='936fcbd3', host='us-cdbr-east-02.cleardb.com', database='heroku_4ac3cade96b682b')
    cursor = connector.cursor(buffered=True)
    values = [str(item) for item in trends]
    #values = ','.join(values)
    #fourth_query = 'UPDATE trendsincities SET trends= ? '.
    cursor.execute('UPDATE trendsincities SET trends = "{}"'.format(values))
    connector.commit()
    print(cursor._last_executed)
    print('Done')
    cursor.close()
    connector.close()

find_current_trends()
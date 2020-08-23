import os
import requests
import pandas as pd
from time import sleep
import mysql.connector
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def find_trends():
    
    bearer = os.environ['BEARER_TOKEN']
    print('trying to connect to server')
    connector = mysql.connector.connect(user='be5852720363b4', password='936fcbd3', host='us-cdbr-east-02.cleardb.com', database='heroku_4ac3cade96b682b')

    if connector.is_connected():    
        cursor = connector.cursor(buffered=True)
        query = 'SELECT * FROM iterator WHERE holder = "it_holder" '
        cursor.execute(query)
        response = cursor.fetchone()
        i = response[1]
        
        if i > 4:
            response = 1
        else:
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

    split_end = i * 70
    split_start = split_end - 70

    trends = [x[6] for x in response]
    woeids = [x[3] for x in response] 
    woeids_copy = woeids
    woeids = woeids[split_start:split_end]
    trends_in_woeids = []
    url = 'https://api.twitter.com/1.1/trends/place.json'
    l2 = []

    for woeid in woeids:
        param = {'id' : woeid}
        response = requests.get(url = url, headers = {'authorization': 'Bearer ' + bearer}, params = param).json()
        l1 = []
        
    try:
        for i in response[0]['trends']:
            l1.append(i['name'])
        l2.append(l1)
    except:
        pass

    print('All trends acquired')

    if len(l2) != 0:
        trends[split_start:split_end] = l2
    
    for num, i in enumerate(trends):
        if type(i) == list:
             trends[num] = ' '.join(i)

    trends = tuple(trends)
    connector = mysql.connector.connect(user='be5852720363b4', password='936fcbd3', host='us-cdbr-east-02.cleardb.com', database='heroku_4ac3cade96b682b')
    cursor = connector.cursor(buffered=True)

    for i, trend in enumerate(trends):
        cursor.execute('UPDATE trendsincities SET trends = %s WHERE woeid = %s', (trend, woeids_copy[i]))

        connector.commit()
    print('Done')
    cursor.close()
    connector.close()

    return None

sched.start()
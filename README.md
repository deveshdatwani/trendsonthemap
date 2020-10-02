## Trends On The Map

### The Webpage
https://www.trendsonthemap.com

### Webpage Snippet

![](https://github.com/deveshdatwani/trendsonthemap/blob/master/trends.PNG) 

### Introduction

Social media has seen exponential growth in the number of its users for about a decade now. More and more people turn to social media to voice their opnions or share parts of their life. Twitter has become a medium on which ideas, opinions and beliefs are shared.

In Twitter, a word, prhase or a hashtag mentioned by a large number of users in a short period of time is said to be "trending topic" or simply "trending" at that point of time. Twitter provides with a funtionality to retrieve the trending topics based on locations through its API.

![]()

A GET request made with authentic API secret key credentials returns JSON file which contains trending topics and in some cases the number of tweets.

### Technologies Used
Python

HTML and CSS

Folium

Jinja2

apschedular

MYSQL


### Installation and Launch (Linux)

From the Terminal, clone the github repository with the command

```
git clone https://github.com/deveshdatwani/trendsonthemap
```

You will also need to set up a mysql server on your machine. Once that is done, import the trendsonthemap schema from the data directory into your msql-server. Do so by using the following command 

```
mysql -u username -p trendsonthemap < file.sql
```

rendsonthemap uses data from this database to access trends. Trends are updated every 90 minutes (more or less).

Then move into the folder with the command

```
cd trendsonthemap
```



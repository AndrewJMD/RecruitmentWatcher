#import and call monkey.patch_all() to solve some issues with the API
import gevent
from gevent import monkey
monkey.patch_all()

#import section
import time, threading
import requests
from bs4 import BeautifulSoup
from steam.client import SteamClient
from steam.enums import EResult

#The interval between checking for new posts
refreshInterval = 15

#ARMA 3 Looking for a unit community forum
unitForumURL = 'https://steamcommunity.com/app/107410/discussions/21/'
#begin as empty string but is used to refrence if the found post is new or not
oldPosts = []
#The URL for the discord Webhook
url = "Replace Discord Webhook Here"

#Creating the steam client
client = SteamClient()
#set location to store sentry files and other stuff
client.set_credential_location(".")

#logs into steam client
client.cli_login()

#creating a web session
session = client.get_web_session()

#allows to reconnect upon error
@client.on("disconnected")
def handle_disconnect():
    if client.relogin_available:
        client.reconnect(maxdelay=30)

@client.on("channel_secured")
def send_login():
    if client.relogin_available:
        client.relogin()

def watchPage():
    global lastPost
    global unitForumURL
    global url
    #storing the response.session in a variable
    x = session.get(unitForumURL)
    #using BeautifulSoup to parse the content of the response
    soup = BeautifulSoup(x.content, 'html.parser')
    forums = soup.find_all('div', class_='forum_topic')
    #finding the first forum that isnt the rules
    forum = forums[1]
    recentPost = forum.find('a', class_='forum_topic_overlay')
    #if the first forum hasnt already been posted
    if recentPost['href'] not in oldPosts:
        oldPosts.append(recentPost['href'])
        #open the post to get a response.session
        x = session.get(recentPost['href'])
        #parse the content of the response to find the form from the OP
        soup = BeautifulSoup(x.content, 'html.parser')
        forum = soup.find('div', class_='forum_op')
        #Find the OPs username, the title and the content text
        username = forum.find('a', class_='forum_op_author')
        title = forum.find('div', class_='topic')
        text = forum.find('div', class_="content")
        #formatting an embed to be posted to discord
        obj = {
          "embeds": [
            {
              "title": str(title.text).strip(),
              "description": str(text.text).strip(),
              "author": {
                "name": str(username.text).strip(),
                "url": recentPost['href']
              }
            }
          ]
        }
        headers = {"Content-Type": "application/json"}
        #posting obj to the webhook and storing it
        x = requests.post(url, headers=headers, json=obj)
        #call self function at set refreshInterval
        threading.Timer(refreshInterval, watchPage).start()
    else:
        #if the new post is the same as the last then ignore it and start timer over
        threading.Timer(refreshInterval, watchPage).start()

#initial call of function
watchPage()

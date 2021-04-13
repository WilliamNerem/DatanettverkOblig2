import urllib.request
import urllib.error
import sys
import bot
import requests

#Når user er i et chat room og en "bot" kjøres, fucker det seg opp. I tillegg vil man få error om man prøver å sende en ny mld


bots = (bot.alice, bot.bob, bot.dora, bot.chuck)
curbot = None
for b in bots:
    if sys.argv[1] == b.__name__:
        curbot = b

BASE = "http://127.0.0.1:5000/"

#user_id = urllib.request.urlopen(BASE + "api/users/" + curbot.__name__)
#requests.get(BASE + "api/users/" + curbot.__name__)
user_id = requests.get(BASE + "api/users/" + curbot.__name__).json()
print(user_id)
room_id = requests.get(BASE + "api/rooms/" + curbot.__name__ +"s%20room").json()
print(room_id)
for i in range(1, room_id+1):
    requests.post(BASE + "api/room/" + str(i) + "/users")
    requests.post(BASE + "api/room/" + curbot() +"/" + str(i) + "/" + str(user_id) + "/messages")
    #message = requests.get(BASE + "api/room/" + str(i) + "/" + str(user_id) + "/fetch").json()
    #print(message)
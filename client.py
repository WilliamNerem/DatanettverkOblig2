import urllib.request
import urllib.error
import sys
import bot

#Når user er i et chat room og en "bot" kjøres, fucker det seg opp. I tillegg vil man få error om man prøver å sende en ny mld


bots = (bot.alice, bot.bob, bot.dora, bot.chuck)
curbot = None
for b in bots:
    if sys.argv[1] == b.__name__:
        curbot = b

BASE = "http://127.0.0.1:5000/"

urllib.request.urlopen(BASE + "api/users/" + curbot.__name__)
urllib.request.urlopen(BASE + "api/rooms/" + curbot.__name__ +"s%20room")
for i in range(10):
    try:
        urllib.request.urlopen(BASE + "api/room/" + str(i) + "/users")
        urllib.request.urlopen(BASE + "/api/room/messages/" + curbot())
    except:
        pass

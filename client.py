import sys
import bot
import requests
import json
import socket

#Når user er i et chat room og en "bot" kjøres, fucker det seg opp. I tillegg vil man få error om man prøver å sende en ny mld


bots = (bot.alice, bot.bob, bot.dora, bot.chuck)
curbot = None
for b in bots:
    if sys.argv[1] == b.__name__:
        curbot = b

BASE = "http://127.0.0.1:5000/"

countRoomsJoined = 0    #holder styr på antall rom klienten er koblet til
serverOnline = True

user_id = requests.get(BASE + "api/users/" + curbot.__name__).json()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(0.00001)

try:
    s.connect(('localhost', 1234))
    s.send(str(user_id).encode())
except:
    serverOnline = False
    s.settimeout(socket.getdefaulttimeout())
    
room_id = requests.get(BASE + "api/rooms/" + curbot.__name__ +"s%20room").json()
for i in range(1, room_id+1):
    requests.post(BASE + "api/room/" + str(i) + "/users")
    countRoomsJoined += 1
    requests.post(BASE + "api/room/" + curbot() +"/" + str(i) + "/" + str(user_id) + "/messages")
    message = requests.get(BASE + "api/room/" + str(i) + "/" + str(user_id) + "/fetch").json()
    out = "Messages in room " + str(i) + ":\n"
    for i in message:
        out += str(i) + "\n"
    print(out)

while serverOnline:
    msg = s.recv(1024).decode() #skal sende alle rom det er nye meldinger i
    '''
    for i in range(countRoomsJoined): #skal svare der det er nye meldinger
        requests.post(BASE + "api/room/" + curbot() +"/" + str(i) + "/" + str(user_id) + "/messages")
        message = requests.get(BASE + "api/room/" + str(i) + "/" + str(user_id) + "/fetch").json()
        out = "Messages in room " + str(i) + ":\n"
        for i in message:
            out += str(i) + "\n"
        print(out)'''
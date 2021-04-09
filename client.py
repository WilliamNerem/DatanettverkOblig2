import urllib.request
import sys

name = sys.argv[1]
roomname = sys.argv[2]

BASE = "http://127.0.0.1:5000/"

urllib.request.urlopen(BASE + "api/users/" + name)
urllib.request.urlopen(BASE + "api/rooms/" + roomname)
for i in range(10):
    try:
        urllib.request.urlopen(BASE + "api/room/" + str(i) + "/users")
        urllib.request.urlopen(BASE + "/api/room/messages/" + "Halla%20jeg%20vil%20ha%20deg%20Martin")
    except urllib.error.HTTPError:
        pass


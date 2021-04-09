import urllib.request
import sys

name = sys.argv[1]
roomname = sys.argv[2]

BASE = "http://127.0.0.1:5000/"

urllib.request.urlopen(BASE + "api/users/" + name)
urllib.request.urlopen(BASE + "api/rooms/" + roomname)
for i in range(100):
    try:
        urllib.request.urlopen(BASE + "api/room/" + str(i) + "/users")
    except:
        pass
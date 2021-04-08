import requests

BASE = "http://127.0.0.1:5000/"


data = [{"name": "King", "rooms": "Green"},
        {"name": "Kong", "rooms": "Pink"},
        {"name": "Long", "rooms": "Cyan"},
        {"name": "Pong", "rooms": "Black"}]

for i in range(len(data)):
    response = requests.put(BASE + "bots/" + str(i), data[i])
    print(response.json())


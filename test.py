import requests

BASE = "http://127.0.0.1:5000/"


data = [{"name": "Gunnar", "rooms": "Yellow, Green"},
        {"name": "Ole", "rooms": "Purple, Pink"},
        {"name": "Kongle", "rooms": "Cyan"}]

for i in range(len(data)):
    response = requests.put(BASE + "bots/" + str(i), data[i])
    print(response.json())


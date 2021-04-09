from Flask import requests

BASE = "http://127.0.0.1:5000/"

response = requests.POST(BASE + "api/users/hei")

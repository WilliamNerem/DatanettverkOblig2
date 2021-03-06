import socket
import time
import requests

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 1234))
s.listen(5)
BASE = "http://127.0.0.1:5000/"
connections = []
connectionsUser_id = []
messageArray = []

def listenEmpty():
    conn, add = s.accept()
    user_id = conn.recv(1024).decode()
    connections.append(conn)
    connectionsUser_id.append(user_id)

def listen():
    stopped = False
    while not stopped:
        try:
            conn, add = s.accept()
            connections.append(conn)
            user_id = conn.recv(1024).decode()
            connectionsUser_id.append(user_id)
        except socket.timeout:
            stopped = True

def checkIfConnected():
    for i in connections:
        try:
            i.send(b'conn?')
        except:
            removeConnection(i)

def removeConnection(a):
    index = connections.index(a)
    connectionsUser_id.pop(index)
    connections.remove(a)

def sendNotification(a):
    listRoomUsers = requests.get(BASE + "api/room/fetchRoomUsers").json()

    for i in listRoomUsers:
        for j in range(len(connections)):
            if str(connectionsUser_id[j]) in str(i):
                connections[j].send(a.encode())
                break

listenEmpty()
listOfMessages = requests.get(BASE + "api/room/fetch").json()
while True:
    listOfRooms = requests.get(BASE + "api/room/fetchRoom_idList").json()
    newListOfMessages = requests.get(BASE + "api/room/fetch").json()
    listOfMessages
    print(newListOfMessages)

    try:
        for i in range(10):
            if newListOfMessages[i] > listOfMessages[i]:
                sendNotification(str(i+1))
    except:
        pass
                
    s.settimeout(0.00001)
    listOfMessages = requests.get(BASE + "api/room/fetch").json()
    listen()
    checkIfConnected()
    if len(connections) == 0:
        s.settimeout(socket.getdefaulttimeout())
        listenEmpty()
    time.sleep(0.1)

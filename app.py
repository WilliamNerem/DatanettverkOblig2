from flask import Flask, request, render_template, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User(username = {username})"
    
class RoomModel(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Room(roomname = {roomname})"

db.drop_all()
db.create_all()

roomMessages = []
listOfMessages = []
listOfUsers = []
messages = []

listRoom = []
listRoomUser = []
listRoomOwner = []
nestedListuser = []
loggedin = ''
currentRoom = ''

class UserMessage:
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"Message(message = {message})"

    def __str__(self):
        return f"Message(message = {message})"    

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('login.html', uservalues=UserModel.query.all())

@app.route("/goback", methods=['GET', 'POST'])
def goBack():
    global nestedListuser
    global loggedin
    return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, loggedin=loggedin, listRoomUser=listRoomUser)

@app.route("/api/users", methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        name=request.form['username']
        user_id=UserModel(username=name)
        user = UserModel(user_id=user_id.user_id, username=name)
        db.session.add(user)
        db.session.commit()
        listOfUsers.append(user.user_id)
        return render_template('login.html', uservalues=UserModel.query.all())
    else: return render_template('login.html', uservalues=UserModel.query.all())

@app.route("/api/users/<string:name>", methods=['GET', 'POST'])
def addclientuser(name):
    global loggedin
    user_id=UserModel(username=name)
    user = UserModel(user_id=user_id.user_id, username=name)
    db.session.add(user)
    db.session.commit()
    loggedin = user.user_id
    listOfUsers.append(user.user_id)
    return str(loggedin)

@app.route("/api/userlogin/<int:user_id>")
def login(user_id):
    global loggedin
    loggedin = user_id
    return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), loggedin=loggedin, listRoomUser=listRoomUser)

@app.route("/api/user/<int:user_id>")
def deleteuser(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        listOfUsers.remove(user.user_id)
        return render_template('login.html', uservalues=UserModel.query.all())
    except: abort(404, message="User ID is not valid")

@app.route("/api/rooms", methods=['GET', 'POST'])
def addroom():
    global listRoom
    global listRoomUser
    global listRoomOwner
    global nestedListuser
    global loggedin
    if request.method == 'POST':
        name=request.form['roomname']
        room_id=RoomModel(roomname=name)
        room = RoomModel(room_id=room_id.room_id, roomname=name)
        db.session.add(room)
        db.session.commit()
        listRoom.append(room.room_id)
        listRoomUser.append([])
        roomMessages.append([])
        return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, loggedin=loggedin, listRoomUser=listRoomUser)
    else: return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, loggedin=loggedin, listRoomUser=listRoomUser)

@app.route("/api/rooms/<string:name>", methods=['GET', 'POST'])
def addclientroom(name):
    global listRoom
    global listRoomUser
    room_id=RoomModel(roomname=name)
    room = RoomModel(room_id=room_id.room_id, roomname=name)
    db.session.add(room)
    db.session.commit()
    listRoom.append(room.room_id)
    listRoomUser.append([])
    roomMessages.append([])
    return str(room.room_id)


@app.route("/api/room/<int:room_id>", methods=['GET'])
def getroom(room_id):
    currentRoom = room_id
    return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, messages=listOfMessages, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages, listRoomUser=listRoomUser)

@app.route("/api/room/<int:room_id>/messages", methods=['GET'])
def onlygetmessage(room_id):
    global nestedListuser
    global loggedin
    global listOfMessages
    a = listRoom.index(room_id)
    listOfMessages = roomMessages[a]
    return render_template('chatroom.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)

@app.route("/api/room/<int:room_id>/<int:user_id>/messages", methods=['GET', 'POST'])
def message(room_id, user_id):
    global nestedListuser
    global loggedin
    global listOfMessages
    if user_id in listOfUsers:
        try:
            if request.method == 'POST':
                inMessage=request.form['message']
                m = UserMessage(user_id, inMessage)
                a = listRoom.index(room_id)
                listOfMessages = roomMessages[a]
                listOfMessages.append(m)
                return render_template('chatroom.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)
            return render_template('chatroom.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)
        except:
            return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)
    else: abort(404, message="User id does not exist")

@app.route("/api/room/<string:message>/<int:room_id>/<int:user_id>/messages", methods=['GET', 'POST'])
def messageclient(message, room_id, user_id):
    global nestedListuser
    global listOfMessages
    try:
        m = UserMessage(user_id, message)
        a = listRoom.index(room_id)
        listOfMessages = roomMessages[a]
        listOfMessages.append(m)
        return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)
    except:
        return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedListuser, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages)


@app.route("/api/room/<int:room_id>/users", methods=['GET', 'POST'])
def roomusers(room_id):
    global listRoomUser
    global listRoom
    global loggedin
    global nestedListuser
    global currentRoom
    try:
        currentRoom = room_id
        a = listRoom.index(room_id)
        nestedListuser = listRoomUser[a]
        nestedListuser.append(loggedin)    
        return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, messages=listOfMessages, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages, listRoomUser=listRoomUser)
    except:
        return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedListuser, messages=listOfMessages, loggedin=loggedin, currentRoom=currentRoom, roomMessages=roomMessages, listRoomUser=listRoomUser)

@app.route("/api/room/<int:room_id>/<int:user_id>/fetch", methods=['GET', 'POST'])
def fetchMessages(room_id, user_id):
    m = UserMessage(user_id, message)
    a = listRoom.index(room_id)
    listOfMessages = roomMessages[a]
    messagesarray = []
    for mes in listOfMessages:
        messagesarray.append(mes.message)
    return jsonify(messagesarray)

@app.route("/api/room/fetch", methods=['GET'])
def fetchAllMessages():
    allMessages = []
    nestedMessages = []
    for i in listRoom:
        allMessages.append([])

    for mes in roomMessages:
        for j in mes:
            allMessages[roomMessages.index(mes)].append(j.message)
    return jsonify(allMessages)

@app.route("/api/room/fetchRoom_idList", methods=['GET'])
def fetchlistOfRoom_id():
    return jsonify(listRoom)

@app.route("/api/room/fetchRoomUsers", methods=['GET'])
def fetchRoomUsers():
    return jsonify(listRoomUser)

if __name__ == "__main__":
    app.run(debug=True)
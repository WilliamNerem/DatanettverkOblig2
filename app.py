from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #/tmp// i en tmp folder evt
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

listOfMessages = []

listRoom = []
listRoomUser = [[]]
nestedList = []
loggedin = 'a'

@app.route("/", methods=['GET', 'POST'])
def index():
    #listOfMessages.clear()
    return render_template('login.html', uservalues=UserModel.query.all())

@app.route("/goback", methods=['GET', 'POST'])
def goBack():
    return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())

@app.route("/api/users", methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        name=request.form['username']
        user_id=UserModel(username=name)
        user = UserModel(user_id=user_id.user_id, username=name)
        db.session.add(user)
        db.session.commit()
        return render_template('login.html', uservalues=UserModel.query.all())
    else: return render_template('login.html', uservalues=UserModel.query.all())

@app.route("/api/users/<string:name>", methods=['GET', 'POST'])
def addclientuser(name):
    global loggedin
    user_id=UserModel(username=name)
    user = UserModel(user_id=user_id.user_id, username=name)
    db.session.add(user)
    db.session.commit()
    loggedin = user_id
    return render_template('login.html', uservalues=UserModel.query.all())

@app.route("/api/userlogin/<int:user_id>")
def login(user_id):
    global loggedin
    loggedin = user_id
    return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())

@app.route("/api/user/<int:user_id>")
def deleteuser(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        if not UserModel.query.all():
            return render_template('login.html', uservalues=UserModel.query.all())
        else:
            return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())
    except: abort(404, message="User ID is not valid")

@app.route("/api/rooms", methods=['GET', 'POST'])
def addroom():
    global listRoom
    global listRoomUser
    if request.method == 'POST':
        name=request.form['roomname']
        room_id=RoomModel(roomname=name)
        room = RoomModel(room_id=room_id.room_id, roomname=name)
        db.session.add(room)
        db.session.commit()
        listRoom.append(room.room_id)
        listRoomUser.append([])
        return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())
    else: return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())

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
    return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())


@app.route("/api/room/<int:room_id>", methods=['GET'])
def getroom(room_id):
    return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages)
    
@app.route("/api/roomdelete/<int:room_id>")
def deleteroom(room_id):
    try:
        listRoomUser.remove(room_id)
        room = RoomModel.query.filter_by(room_id=room_id).delete()
        db.session.commit()
        return render_template('index.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all())
    except: abort(404, message="Room ID is not valid")

@app.route("/api/room/messages", methods=['GET', 'POST'])
def message():
    global nestedList
    global loggedin
    if request.method == 'POST':
        inMessage=request.form['message']
        listOfMessages.append(inMessage)
        return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedList, loggedin=loggedin)
    return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), messages=listOfMessages, listUsers=nestedList, loggedin=loggedin)

@app.route("/api/room/<int:room_id>/users", methods=['GET', 'POST'])
def roomusers(room_id):
    global listRoomUser
    global listRoom
    global loggedin
    global nestedList
    a = listRoom.index(room_id)
    nestedList = listRoomUser[a]
    nestedList.append(loggedin)
    #print(listRoomUser, file=sys.stderr)
    return render_template('room.html', uservalues=UserModel.query.all(), roomvalues=RoomModel.query.all(), listUsers=nestedList, messages=listOfMessages, loggedin=loggedin)

if __name__ == "__main__":
    app.run(debug=True)
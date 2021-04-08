from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #/tmp// i en tmp folder evt
db = SQLAlchemy(app)

class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"User(name = {name})"
    
class RoomModel(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f"Room(name = {name})"
db.drop_all()
db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', values=UserModel.query.all())

@app.route("/api/users", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        name=request.form['name']
        user_id=UserModel(name=name)
        user = UserModel(user_id=user_id.user_id, name=name)
        db.session.add(user)
        db.session.commit()
        return render_template('index.html', values=UserModel.query.all())
    else: return render_template('index.html', values=UserModel.query.all())

@app.route("/api/user/<int:user_id>")
def delete(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return render_template('index.html', values=UserModel.query.all())
    except: abort(404, message="Bot ID is not valid")

if __name__ == "__main__":
    app.run(debug=True)
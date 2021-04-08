from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #/tmp// i en tmp folder evt
db = SQLAlchemy(app)

class BotModel(db.Model):
    bot_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    rooms = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Bot(name = {name}, rooms = {rooms})"
    
db.drop_all()
db.create_all()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html', values=BotModel.query.all())

@app.route("/api/users", methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        name=request.form['name']
        rooms=request.form['rooms']
        bot_id=BotModel(name=name, rooms=rooms)
        bot = BotModel(bot_id=bot_id.bot_id, name=name, rooms=rooms)
        db.session.add(bot)
        db.session.commit()
        return render_template('index.html', values=BotModel.query.all())
    else: return render_template('index.html', values=BotModel.query.all())

@app.route("/api/user/<int:user_id>")
def delete(user_id):
    try:
        bot = BotModel.query.filter_by(bot_id=user_id).delete()
        db.session.commit()
        return render_template('index.html', values=BotModel.query.all())
    except: abort(404, message="Bot ID is not valid")

if __name__ == "__main__":
    app.run(debug=True)
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
def test():
    if request.method == 'POST':
        bot = BotModel(name="Yolo", rooms="Black")
        db.session.add(bot)
        db.session.commit()
        return render_template('index.html', values=BotModel.query.all())
    else: return render_template('index.html', values=BotModel.query.all())


bot_put_args = reqparse.RequestParser() # Forsikrer at det passer med hvordan man vil parse som defineres senere
bot_put_args.add_argument("name", type=str, help="Name of the bot is required", required=True) # Argumentet må være med hvis ikke displayes Help som er feilmelding
bot_put_args.add_argument("rooms", type=str, help="Room for the bot is required", required=True)

bots = {}

resource_fields = {
    'bot_id': fields.Integer,
    'name': fields.String,
    'rooms': fields.String
}

def wrong_botid(bot_id):
    if bot_id not in bots:
        abort(404, message="Bot ID is not valid") # Sending error message back, need to send status code


def botid_exists(bot_id):
    if bot_id in bots:
        abort(409, message="Bot ID already taken")

class Bot(Resource): # Method names are matching the http requests such as get, put, delete
    def get(self, bot_id):
        wrong_botid(bot_id) # It won't go to return, stops here
        return bots[bot_id]

    @marshal_with(resource_fields)
    def put(self):
        args = bot_put_args.parse_args()
        bot = BotModel(name=args['name'], rooms=args['rooms'])
        db.session.add(bot)
        db.session.commit()
        return bot, 201  # 201 is created, 200 is okey

    def delete(self, bot_id):
        wrong_botid(bot_id)
        del bots[bot_id]
        return '', 204 # 204 is deleted successfully

api.add_resource(Bot, "/bots/<int:bot_id>") # What they put as parameter in bot_id will become the bot_id in the put request, and the key in the dictonary

if __name__ == "__main__":
    app.run(debug=True)
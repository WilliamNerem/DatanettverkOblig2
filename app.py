from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

bot_put_args = reqparse.RequestParser() # Forsikrer at det passer med hvordan man vil parse som defineres senere
bot_put_args.add_argument("name", type=str, help="Name of the bot is required", required=True) # Argumentet må være med hvis ikke displayes Help som er feilmelding
bot_put_args.add_argument("rooms", type=str, help="Room for the bot is required", required=True)

bots = {}

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

    def put(self, bot_id):
        botid_exists(bot_id)
        args = bot_put_args.parse_args()
        bots[bot_id] = args
        return bots[bot_id], 201  # 201 is created, 200 is okey

    def delete(self, bot_id):
        wrong_botid(bot_id)
        del bots[bot_id]
        return '', 204 # 204 is deleted successfully

api.add_resource(Bot, "/bots/<int:bot_id>") # What they put as parameter in bot_id will become the bot_id in the put request, and the key in the dictonary

if __name__ == "__main__":
    app.run(debug=True)
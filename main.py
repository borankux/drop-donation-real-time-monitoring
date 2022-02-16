import time
import requests as rq
import json
from flask import Flask
from flask import render_template
from playsound import playsound
import redis

client = redis.Redis()

def get_amount():
    api = "https://api.shuidichou.com/api/cf/v4/user/get-user-case-info"
    payload = {
        'infoUuid': 'c450594b-c112-4e45-97fb-5a922272c59d'
    }
    jsonData = rq.post(url=api, data=payload).content
    data = json.loads(jsonData)
    a = data['data']['caseBaseInfo']['amount']
    return a / 100


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/amount')
def amount():
    a = get_amount()
    payed = int(a)
    previous = int(client.get("amount"))
    if payed != previous:
        client.set("amount", payed)
    return str(a)


app.run(port=8080)


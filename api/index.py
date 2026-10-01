import os
from flask import Flask, request, jsonify
from python_aternos import Client

app = Flask(__name__)

ACCESS_KEY = os.environ["ACCESS_KEY"]          # secret key you invent
ATERNOS_USER = os.environ["ATERNOS_USER"]
ATERNOS_PASS = os.environ["ATERNOS_PASS"]


def get_server():
    client = Client()
    client.login(ATERNOS_USER, ATERNOS_PASS)
    servers = client.account.list_servers()
    return servers[0]  # adjust index if you have multiple servers


def authorized():
    return request.args.get("key") == ACCESS_KEY


@app.route("/status")
def status():
    if not authorized():
        return jsonify(error="unauthorized"), 401
    s = get_server()
    return jsonify(status=str(s.status))


@app.route("/start")
def start():
    if not authorized():
        return jsonify(error="unauthorized"), 401
    s = get_server()
    if str(s.status) == "online":
        return jsonify(status="already online")
    s.start()
    return jsonify(status="start requested")


# Vercel needs the raw Flask app exposed
app_handler = app
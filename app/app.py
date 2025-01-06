import sqlite3
import os
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from dotenv import load_dotenv

import settings


app = Flask(__name__)
auth = HTTPTokenAuth(scheme="Bearer")

CORS(app)

load_dotenv()

@auth.verify_token
def verify_api_key(api_key):
    return True if api_key == os.getenv("key") else False

@app.route("/")
# @auth.login_required
def index():
    return "Hello, World !"


# services for portfolio (jiemcode.github.io)
@app.route("/portfolio/message_handler", methods=["POST"])
@auth.login_required
def msg_handler():
    if request.method == "POST":
        print(request.is_json)
        data = request.json
        username = data.get("firstame", "")
        email = data.get("email", "")
        message = data.get("message", "")

        print(f"F: {username} - E: {email} - M: {message}")
        
        conn = sqlite3.connect(settings.DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (username, email, message)
            VALUES (?, ?, ?)
        ''', (username, email, message))
        conn.commit()
        conn.close()

        return "Posted"
    

@app.route("/portfolio/messages", methods=["GET"])
# @auth.login_required
def message():
    if request.method == "GET":
        conn = sqlite3.connect(settings.DB)
        cursor = conn.cursor()
        cursor.execute('SELECT username, email, message, date FROM messages')
        messages = cursor.fetchall()
        conn.close()

        message_list = [{"username": msg[0], "email": msg[1], "message": msg[2], "date": msg[3]} for msg in messages]
        return {"messages": message_list}


@app.route("/cpuam/notifications/get", methods=["POST"])
def get_notifications():
    if request.method == "POST":
        data = request.json

        status = request.POST['data']['status']
        amount = request.POST['data']['invoice']['total_amount']
        hash = request.POST['data']['hash']
        content = request.POST['data']
        
        
        conn = sqlite3.connect(settings.DB)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (status, amount, hash, content)
            VALUES (?, ?, ?, ?)
        ''', (status, amount, hash, content))
        conn.commit()
        conn.close()

        return "Saved"


@app.route("/cpuam/notifications", methods=["POST"])
def list_notifications():
    if request.method == "GET":
        conn = sqlite3.connect(settings.DB)
        cursor = conn.cursor()
        cursor.execute('SELECT username, email, message, date FROM messages')
        messages = cursor.fetchall()
        conn.close()

        message_list = [{"username": msg[0], "email": msg[1], "message": msg[2], "date": msg[3]} for msg in messages]
        return {"messages": message_list}


if __name__ == "__main__":

    host = "localhost"
    port = 8080

    app.run(host, port, debug=True)
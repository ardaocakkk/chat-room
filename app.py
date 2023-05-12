from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send



users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on("connect")
def test_connect():
    print("Client connected")

@socketio.on("join")
def handle_message(username):
    users[username] = request.sid
    print("Current user: " + username)

@socketio.on("message")
def handle_message(message):
    username = ""
    for user in users:
        if users[user] == request.sid:
            username = user

    emit("chat", {"message": message, "username": username}, broadcast=True)


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)
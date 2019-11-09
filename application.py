import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('user_connects')
def handle_user_connects(data):
    print('received message: ' + data['message'])
    emit('connection_response', data, broadcast=True)


@socketio.on('message_send')
def handle_message_send(data):
    print('Send button was clicked!')
    emit('message_update', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

import os

from time import localtime, strftime
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from flask import Flask, render_template, request, abort, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room

allowed_users = ['foo', 'bar', 'Keegan']
ROOMS = ['lounge', 'news', 'games', 'coding']

app = Flask(__name__)
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SECRET_KEY"] = 'abcdefghijkl'

login_manager = LoginManager(app)
socketio = SocketIO(app)


@login_manager.user_loader
def user_loader(id):
    return User(id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@app.route("/")
def index():
    return render_template("index.html", username=current_user.get_id(), rooms=ROOMS)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username not in allowed_users:
            abort(401)
        login_user(User(username))
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    if current_user.is_anonymous:
        return redirect("/login")
    data = {'message': "** DISCONNECTED **",
            'username': current_user.get_id(),
            'timestamp': strftime('%b-%d %I:%M%p', localtime())}
    socketio.emit('message_update', data, broadcast=True)
    logout_user()
    print("logout triggered")
    return redirect("/login")


@socketio.on('user_connects')
def handle_user_connects(data):
    if current_user.is_anonymous:
        return redirect("/login")
    data = {'message': ">> CONNECTED <<",
            'username': current_user.get_id(),
            'timestamp': strftime('%b-%d %I:%M%p', localtime())}
    print("All this bullshit: ")
    print(data)
    emit('message_update', data, broadcast=True)


@socketio.on('message_send')
def handle_message_send(data):
    room = data['room']
    data = {'message': data['message'],
            'username': current_user.get_id(),
            'timestamp': strftime('%b-%d %I:%M%p', localtime())}
    emit('message_update', data, room=room, broadcast=True)


@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)
    data = {'message': data['username'] + " has joined " + data['room'],
            'username': current_user.get_id(),
            'timestamp': strftime('%b-%d %I:%M%p', localtime())}
    emit('message_update', data, room=room, broadcast=True)


@socketio.on('leave')
def leave(data):
    room = data['room']
    leave_room(room)
    data = {'message': data['username'] + " has left " + data['room'],
            'username': data['username'],
            'timestamp': strftime('%b-%d %I:%M%p', localtime())}
    emit('message_update', data, room=room, broadcast=True)


@socketio.on('create_channel')
def handle_create_channel(data):
    if data['channel'] in ROOMS:
        return False
    else:
        ROOMS.append(data['channel'])
        #channels[data['channel']] = []
    emit('channel_update', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

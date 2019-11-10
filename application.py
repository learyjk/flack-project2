import os

from time import localtime, strftime
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from flask import Flask, render_template, request, abort, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room

allowed_users = ['foo', 'bar', 'Keegan']
ROOMS = ['Lounge', 'News', 'Games', 'Coding']
MESSAGES = {}
LIMIT = 100

for room in ROOMS:
    MESSAGES[room] = []

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
    if current_user.is_anonymous:
        return redirect("/login")
    return render_template("index.html", username=current_user.get_id(), rooms=ROOMS, messages=MESSAGES[room])


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

        # doesn't work because have no way to get room in this route.
    # time_stamp = strftime('%b-%d %I:%M%p', localtime())
    # message = time_stamp + " " + current_user.get_id() + " has left the room."
    # MESSAGES[room].append(message)

    logout_user()
    print("logout triggered")
    return redirect("/login")


@socketio.on('user_connects')
def handle_user_connects(data):
    if current_user.is_anonymous:
        return redirect("/login")


@socketio.on('message_send')
def handle_message_send(data):
    room = data['room']

    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    message = time_stamp + " " + data['username'] + ": " + data['message']

    MESSAGES[room].append(message)
    # don't store more than 100 previous messages
    if len(MESSAGES[room]) > LIMIT:
        MESSAGES[room].pop(0)

    data = {'message': message}
    emit('message_update', data, room=room, broadcast=True)


@socketio.on('join')
def join(data):
    room = data['room']
    join_room(room)

    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    message = time_stamp + " " + data['username'] + " has joined " + room

    MESSAGES[room].append(message)
    # don't store more than 100 previous messages
    if len(MESSAGES[room]) > LIMIT:
        MESSAGES[room].pop(0)

    data = {'previous_messages': MESSAGES[room]}

    emit('message_update', data, room=room, broadcast=True)


@socketio.on('leave')
def leave(data):
    room = data['room']
    leave_room(room)

    time_stamp = strftime('%b-%d %I:%M%p', localtime())
    message = time_stamp + " " + data['username'] + " has left " + room

    MESSAGES[room].append(message)
    # don't store more than 100 previous messages
    if len(MESSAGES[room]) > LIMIT:
        MESSAGES[room].pop(0)

    data = {'message': message}
    emit('message_update', data, room=room, broadcast=True)


@socketio.on('create_channel')
def handle_create_channel(data):
    room = data['channel'].title()
    if room in ROOMS:
        data = {'message': "Room already exists!"}
        emit('message_update', data, broadcast=True)
    else:
        ROOMS.append(room)
        MESSAGES[room] = []

        emit('channel_update', {'channel': room}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

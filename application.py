import os

from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin
from flask import Flask, render_template, request, abort, redirect
from flask_socketio import SocketIO, emit

allowed_users = ['foo', 'bar', 'Keegan']

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
    return render_template("index.html")


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
    data = {'message': current_user.get_id() + " has disconnected."}
    socketio.emit('message_update', data, broadcast=True)
    logout_user()
    print("logout triggered")
    return redirect("/login")


@socketio.on('user_connects')
def handle_user_connects(data):
    if current_user.is_anonymous:
        return redirect("/login")
    print(data['message'])
    data['message'] = current_user.get_id() + " has connected."
    emit('message_update', data, broadcast=True)


@socketio.on('message_send')
def handle_message_send(data):
    print('Send button was clicked!')
    data['message'] = current_user.get_id() + ": " + data['message']
    emit('message_update', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)

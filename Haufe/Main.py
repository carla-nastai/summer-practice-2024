
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_socketio import SocketIO, join_room, leave_room, send, emit

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Original50!@localhost/Proiect'
app.config['SECRET_KEY'] = 'scrt123fasd'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'carla.nastai@gmail.com'
app.config['MAIL_PASSWORD'] = 'ohqp yqpz yvcb syqn'

socketio = SocketIO(app)
user_rooms = {}


db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nume = db.Column(db.String(40), nullable=False)
    prenume = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Film(db.Model):
    __tablename__='filme'
    nume = db.Column(db.String(40), primary_key=True, autoincrement=True)
    recom = db.Column(db.String(40), nullable=False)
    descript = db.Column(db.String(40), nullable=False)
    link = db.Column(db.String(120), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)


#####
@app.route('/')
def Main_page():
    return render_template('Home.html')

@app.route('/chatroom/<group_name>')
def chatroom(group_name):
    return render_template('chatroom.html', group_name=group_name)

@socketio.on('join_room')
def handle_join_room(data):
    group_name = data['group_name']
    join_room(group_name)
    emit('doctor_joined', room=group_name)
    print(f'user has joined group {group_name}')
    emit('status', {'msg': f'user has joined the chat.'}, group=group_name)

@socketio.on('send_message')
def handle_send_message(data):
    message = data['message']
    group_name = data['group_name']
    emit('receive_message', {'message': message}, room=group_name)
    print(f'Message sent to room {group_name}: {message}')
##########


@app.route('/Home.html')
def Home():
    return render_template('Home.html')

@app.route('/Recenzie.html')
def Recenzie():
    return render_template('Recenzie.html')

@app.route('/Chat.html', methods=['GET', 'POST'])
def chat_selection():
    if request.method == 'POST':
        # Get form data
        user_email = request.form['user'] ##
        group_name = request.form['group_name']

        # Send email to user with chat room link
        send_chat_link_email(user_email, group_name)

        # Redirect to chat room with room number
        return redirect(url_for('chatroom', group_name=group_name))

    return render_template('Chat.html', User=User)
def send_chat_link_email(user_email, group_name):
    # Construct the chat room URL
    chat_room_url = url_for('chatroom', group_name=group_name, _external=True)

    user_email = request.cookies.get('user_email')

    msg = Message('Chat Room', sender='carla.nastai@gmail.com', recipients=[user_email])
    msg.body = f'You have a Chat request with {user_email}. Join the chat using this link: {chat_room_url}'
    mail.send(msg)


if __name__ == '__main__':
    socketio.run(app, debug=True,allow_unsafe_werkzeug=True)
    app.run(debug=True)

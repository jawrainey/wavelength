from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secretsecretsecretterces'
socketio = SocketIO(app)

# ??
available_rooms = []
# ??
listeners = {}
# Should contain a map {img:text, img:text, img:text}
selected_imgs = []


@app.route("/",  methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'Speaker' in request.form['submit']:
            session['role'] = 'speaker'
            return redirect(url_for('selection'))
        else:
            session['role'] = 'listener'
        return redirect(url_for('chat'))
    return render_template('index.html')


@app.route("/role",  methods=['POST'])
def role():
    if request.method == 'POST':
        session['role'] = request.form['role']
        return redirect(url_for('chat'))


@app.route("/selection", methods=['GET', 'POST'])
def selection():
    import os
    files = os.listdir(os.path.join(app.static_folder, 'img/selection'))
    if request.method == 'POST':
        # TODO: Receive selected images & populate 'selected_imgs'
<<<<<<< HEAD
        for item in request.form:
            print item, type(item)
        a = [item[1] for item in request.form]
        print a
=======
>>>>>>> 983fdcdc8e43309fa351d2957babf8553972031d
        return redirect(url_for('input'))
    return render_template('selection.html', imgs=files)


@app.route("/input", methods=['GET', 'POST'])
def input():
    # Populate the form with the 'selected imgs'
    if request.method == 'POST':
        return redirect(url_for('chat'))
    files = ['1.jpg', '2.jpg', '3.jpg']
    return render_template('input.html', imgs=files)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    # Populate the form with the image AND text...
    files = {'1.jpg': 'lots of text', '2.jpg': 'lots of text2', '3.jpg': 'lots of 3'}
    return render_template('chat.html', imgs=files)


@socketio.on('start', namespace='/chat')
def room_selection(message):
    # Sent by clients (users) when they select a role (speaker/listener)
    role = session.get('role')
    # The speakers room is going to be the sessionID /chat/<sid>
    sid = request.sid

    # This is where 'smart' match-making should occur:
    # TODO: match un-matched listeners to speakers...

    # For simplicity, match listeners to the last available speaker...
    if 'speaker' in role:
        join_room(sid)
        available_rooms.append(sid)
        emit('status', {'message': 'Welcome speaker..'}, room=sid)
    else:
        # Find available speakers...
        # IF a saved speaker is not in the listeners list, then
        # we have a free speaker to chat to!
        # This is only used for a count...

        if available_rooms:
            import random
            room = random.choice(available_rooms)
            join_room(room)
            listeners[sid] = room
            emit('status', {'message': 'Joined speaker in ' + str(room)},
                 room=room)
            available_rooms.remove(room)
        else:
            emit('status', {'message': 'No speakers free. Check back later...'})


@socketio.on('message', namespace='/chat')
def message(message):
    # Send the client message to all people in the room.
    # Everything 'message' to add to the confusion of message passing.
    # request.sid will only work if it's the speaker sending a message...
    # if it's a listener, then a lookup (associated room) needs to be made.
    role = session['role']
    if 'listener' in role:
        room = listeners[request.sid]
    else:
        room = request.sid
    emit('message', {'message': message,'role': role}, room=room)

if __name__ == "__main__":
    socketio.run(app)

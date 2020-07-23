from flask import Flask,render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'theesecret'
socketio = SocketIO( app )

@app.route('/')
def index():    
    title = 'TicTacToe Messenger'

    return render_template('index.html', title = title)

@socketio.on('my event')
def handle_my_custom_event( json ):
    print( 'message: ' + str(json) )
    socketio.emit( 'my response', json, broadcast = True )

if __name__ == '__main__':
    socketio.run(app, debug= True)

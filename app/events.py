from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, render_template, request, json
from flask_session import Session

from . import socketio
from itertools import permutations


all_rooms = []
rooms_data = []
list_of_possible_wins = [
            [1,2,3],
            [4,5,6],
            [7,8,9],
            [1,4,7],
            [2,5,8],
            [3,6,9],
            [3,5,7],
            [1,5,9]
        ]
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json['data']))
    emit('my response', 'Nice', broadcast= True)

@socketio.on('new message')
def show_message(data):
    emit('show message', data['data'], broadcast = True)

@socketio.on('create game')
def create_game(data):
    room_id = data['game_id']
    user_id = request.sid
    user = [user_id]
    
    if all_rooms.count(room_id) > 0:
        a_room_to_check = None
        for room in rooms_data:
            if room['id'] == room_id:
                a_room_to_check = room
            
        if a_room_to_check is not None and len(a_room_to_check['users']) < 2:
            users = a_room_to_check['users']
            users.append(user_id)
            a_room_to_check['game'] = {
                'played_moves': [],
                users[0]: [],
                users[1]: []
            }
            join_room(a_room_to_check['id'])

            emit('other play', 'Game about to start.', room = a_room_to_check['id'])
            emit('start', {'played': False}, room = users[0])
        else:
            emit('back home',  room = request.sid)

    else:
        a_room = {
            'id': room_id,
            'users': user
        }
        all_rooms.append(a_room['id'])
        rooms_data.append(a_room)

        join_room(a_room['id'])

        rooms = json.dumps(all_rooms)
        emit('play', rooms,  room = user_id)

@socketio.on('played')
def play(data):
    if all_rooms.count(data['game']) > 0:
        room_to_play = None
        for room in rooms_data:
            for user in room['users']:
                if user == request.sid:
                    room_to_play = room
                    game = room_to_play['game']
                else:
                    other_user = user

        if len(game['played_moves']) <= 8 :
            if game['played_moves'].count(data['play']) < 1:
                game[request.sid].append(data['play'])
                game['played_moves'].append(data['play'])

                if request.sid == room_to_play['users'][0]:
                    emit('spot picked', {'spot': data['play'], 'show': 'X'}, room = room_to_play['id'])
                else:
                    emit('spot picked', {'spot': data['play'], 'show': 'O'}, room = room_to_play['id'])


                all = list(permutations(game[request.sid], 3))
                for i in all:
                    for j in list_of_possible_wins:
                        i = set(i)
                        j = set(j)
                        if i == j:
                            print('Caught')
                            print(i)
                            emit('won', request.sid, room = request.sid)           
                            emit('lost', request.sid, room = other_user )
                            break
                    break     
                print(game)
                other_player = None
                for user in room_to_play['users']:
                    if user != request.sid:    
                        my_played_moves = json.dumps(game[user])
                        if len(game['played_moves']) > 8:
                            print('Game over for now.')
                            print(game)
                            emit('draw', room = room_to_play['id'])
                            break
                        emit('start',my_played_moves , room = user)
                        break
            else:
                emit('start', {'played': True, 'play': data['play']} , room = request.sid)

        else:
            emit('draw', room = room_to_play['id'])
            print('Game over for now.')
            print(game)
    else:

        #TODO Handle wrong game id -> (Wrong link)
        emit('error', room = request.sid)

from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Flask, render_template, request, json, url_for, redirect
from itertools import permutations
import jsonpickle

from . import socketio
from . import red



all_rooms = []
rooms_data = []
list_of_possible_wins = [
            ['1','2','3'],
            ['4','5','6'],
            ['7','8','9'],
            ['1','4','7'],
            ['2','5','8'],
            ['3','6','9'],
            ['3','5','7'],
            ['1','5','9']
        ]

@socketio.on('create game')
def create_game(data):
    game = data['game_id']
    user = data['user_id']
    print(red.get(game))
    
    if red.exists(game):
        print('Game is live bruv!')
        game_play = 'game_' + game
        user_game = 'user_game_' + user
        print(red.smembers(user_game))
        played_moves = 'played_moves_' + game

        if red.exists(game_play):
            if red.hexists(game_play, 'p2'):
                if  red.hget(game_play, 'p1') == user or red.hget(game_play, 'p2') == user:
                    print('My id is')
                    print(user)
                    red.delete(user_game)
                    red.delete(played_moves)
                    p1_prev_scores = int(red.hget(game_play, 'p1W'))
                    p2_prev_scores = int(red.hget(game_play, 'p2W'))
                    total_games_played = int(red.hget(game_play, 'total'))
                    
                    print(total_games_played)
                    if p1_prev_scores == 0 and p2_prev_scores == 0:
                        socketio.emit('start', 'Player 1 starts.', room = red.hget(game_play, 'p1'))
                    elif p1_prev_scores == p2_prev_scores:
                        if total_games_played  % 2 != 0:
                            socketio.emit('start', 'Your turn to start.', room = red.hget(game_play, 'p1'))
                        else:
                            socketio.emit('start', 'Your turn to start.', room = red.hget(game_play, 'p2'))
                    elif p1_prev_scores > p2_prev_scores:
                        socketio.emit('start', 'Winner starts.', room = red.hget(game_play, 'p1'))
                    else:
                        socketio.emit('start', 'Winner starts.', room = red.hget(game_play, 'p2')) 
                else:
                    join_room(user)
                    socketio.emit('back home', room = user)
                    leave_room(user)
                    return 
            else:
                print("Good! You can join!!")

                red.hset(game_play, 'p2', user)
                red.hset(game_play, 'p2W', 0)
                red.hset(game_play, 'p2L', 0)
                red.hset(game_play, user_game, user_game)
                print(red.hgetall(game_play))
                join_room(game_play)
                join_room(red.hget(game_play, 'p2'))


                p1_prev_scores = int(red.hget(game_play, 'p1W'))
                p2_prev_scores = int(red.hget(game_play, 'p2W'))
                total_games_played = int(red.hget(game_play, 'total'))
                
                print(total_games_played)
                if p1_prev_scores == 0 and p2_prev_scores == 0:
                    socketio.emit('connected', 'Successfully passed data',  room = game_play)
                    socketio.emit('start', 'Player 1 starts.', room = red.hget(game_play, 'p1'))
                elif p1_prev_scores == p2_prev_scores:
                    if total_games_played  % 2 != 0:
                        socketio.emit('start', 'Your turn to start.', room = red.hget(game_play, 'p1'))
                    else:
                        socketio.emit('start', 'Your turn to start.', room = red.hget(game_play, 'p2'))
                elif p1_prev_scores > p2_prev_scores:
                    socketio.emit('start', 'Winner starts.', room = red.hget(game_play, 'p1'))
                else:
                    socketio.emit('start', 'Winner starts.', room = red.hget(game_play, 'p2'))
        else:
            red.hset(game_play, 'p1', user)
            red.hset(game_play, 'p1W', 0)
            red.hset(game_play, 'p1L', 0)
            red.hset(game_play, user_game, user_game)
            red.hset(game_play, 'total', 0)

            print(red.hgetall(game_play))
            join_room(game_play)
            join_room(red.hget(game_play, 'p1'))

            socketio.emit('invite', 'Invite your friend to play', room = game_play)

@socketio.on('played')
def played_moves(data):
    user = data['user']
    game = data['game']
    play = data['play']
    user_play = 'user_game_' + user
    
    if red.exists(game): #Game is valid
        game_play = 'game_' + game
        played_moves = 'played_moves_' + game

        
        if red.hget(game_play,'p1') == user: #Check that player one is the one who has played. 

            if red.scard(played_moves) < 9 : # No. of plays not exceeded.

                if not red.sismember(played_moves, str(play)): #Move not played before.
                    red.sadd(played_moves, str(play))
                    red.sadd(user_play, str(play))
                    socketio.emit('spot picked', {'spot': play, 'show': 'X'}, game_play )
                    print(red.smembers(played_moves))
                    print(red.smembers(user_play))
                    user_plays = red.smembers(user_play)

                    all = list(permutations(user_plays, 3))

                    for i in all:
                        for j in list_of_possible_wins:
                            
                            i = set(i)
                            j = set(j)
                            if i == j:
                                print('Caught')
                                print(i)
                                red.delete(user_play)
                                red.delete(played_moves)
                                red.hincrby(game_play, 'p1W', amount = 1)
                                red.hincrby(game_play, 'p2L', amount = 1)
                                socketio.emit('clear', room = game_play)
                                win_play_str = ''
                                for num in j:
                                    win_play_str += str(num) + ','
                                emit('won', {'winner':'p1','set': win_play_str}, room = red.hget(game_play, 'p1') )           
                                emit('lost',{'loser':'p2', 'set': win_play_str}, room = red.hget(game_play, 'p2') )
                                emit('play again', 'Do you want to play again?', room = game_play)
                                return     
                    if red.scard(played_moves) > 8:
                        socketio.emit('draw', room = game_play )
                        socketio.emit('clear', room = game_play)
                    else:
                        
                        socketio.emit('start',{'message': 'Your turn'}, room = red.hget(game_play, 'p2'))

                elif red.sismember(played_moves, str(play)): #Move already played.
                    socketio.emit('start', {'played': True, 'message': 'Sorry that has already been played.'}, room = red.hget(game_play, 'p1'))
            else:
                red.delete(user_game)
                red.delete(played_moves)
                socketio.emit('draw','Oopsies it is a draw', room = game_play ) #No of plays exceeded.
                socketio.emit('clear', room = game_play)
                  
        elif red.hget(game_play, 'p2') == user:
            
            if red.scard(played_moves) < 9 : # No. of plays not exceeded.

                if not red.sismember(played_moves, str(play)): #Move not played before.

                    red.sadd(played_moves, str(play))
                    red.sadd(user_play, str(play))
                    socketio.emit('spot picked', {'spot': play, 'show': 'O'}, game_play )
                    print(red.smembers(played_moves))
                    print(red.smembers(user_play))

                    user_plays = red.smembers(user_play)

                    all = list(permutations(user_plays, 3))

                    for i in all:
                        for j in list_of_possible_wins:
                            
                            i = set(i)
                            j = set(j)

                            if i == j:
                                print('Caught')
                                print(i)
                                red.delete(user_play)
                                red.delete(played_moves)
                                red.hincrby(game_play, 'p2W', amount = 1)
                                red.hincrby(game_play, 'p1L', amount = 1)
                                socketio.emit('clear', room = game_play)
                                win_play_str = ''
                                for num in j:
                                    win_play_str += str(num) + ','
                                emit('won', {'winner': 'p2', 'set': win_play_str}, room = red.hget(game_play, 'p2') )           
                                emit('lost', {'loser': 'p1', 'set': win_play_str}, room = red.hget(game_play, 'p1') )
                                emit('play again', 'Do you want to play again?', room = game_play)     

                                return
                    if red.scard(played_moves) > 8:
                        socketio.emit('draw', room = game_play )
                        socketio.emit('clear', room = game_play)
                    else:
                        
                        socketio.emit('start',{'message': 'Your turn'}, room = red.hget(game_play, 'p1'))

                elif red.sismember(played_moves, str(play)): #Move already played.
                    socketio.emit('start', {'played': True, 'message': 'Sorry that has already been played.'}, room = red.hget(game_play, 'p2'))
            else:

                red.delete(user_play)
                red.delete(played_moves)
                socketio.emit('draw', room = game_play ) #No of plays exceeded.
                socketio.emit('clear', room = game_play)



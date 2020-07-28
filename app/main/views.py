from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..requests import search
from .forms import SearchSong
import uuid

from .. import red

# from ..models import

@main.route('/', methods  = ['GET', 'POST'])
def index():
    '''
    Homepage
    '''
    title = "TicTacToe"

    if request.method == 'POST':
        unique_id = str(uuid.uuid1())
        if not red.exists(unique_id):
            print("Nada exists")
            red.set(unique_id, unique_id)
            return redirect(url_for('main.create_game', id = unique_id))
        else:
            error = "Something wrong happened. Please try again."
            return render_template('index.html', error = error)

    return render_template('index.html', title = title)


@main.route('/<id>')
def create_game(id):

    title = "TicTacToe"

    if red.exists(id):
        user_id = str(uuid.uuid1())
        print("Now exists")

        return render_template('game.html', game_id = id, user_id = user_id, title = title)
    
    else:
        return redirect(url_for('main.index'))


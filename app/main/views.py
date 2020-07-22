from flask import render_template, request, redirect, url_for, abort, flash
from . import main
# from ..models import

@main.route('/')
def index():
    '''
    Homepage
    '''

    title = "TicTacToe"

    return render_template('index.html', title = title)

@main.route('/game/')
def game():
    '''
    Game page
    '''

    title = "TicTacToe"

    return render_template('game.html', title = title)
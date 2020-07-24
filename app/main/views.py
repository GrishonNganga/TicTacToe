from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..requests import search
from .forms import SearchSong

# from ..models import

@main.route('/', methods=['GET','POST'])
def index():
    '''
    Homepage
    '''
    title = "TicTacToe"
    form = SearchSong()
    search_song = form.search_item.data

    if search_song:
        return redirect(url_for('.tafuta', search_song=search_song))
    else:
        return render_template('index.html', title = title, form=form)


@main.route('/search/<search_song>',methods=['GET','POST'])
def tafuta(search_song):
    form = SearchSong()
    song_name = search(search_song)

    print(song_name)
    return render_template('index.html', song_name=song_name, form=form)
    # return render_template('index.html', title = title)

@main.route('/game/')
def game():
    '''
    Game page
    '''

    title = "TicTacToe"

    return render_template('game.html', title = title)

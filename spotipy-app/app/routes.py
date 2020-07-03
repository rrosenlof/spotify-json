from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import UsernameForm, CollageForm
from auth import show_playlists, get_tracks, get_playlist

@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        user = session['username']
        playlists = show_playlists(user)
        return render_template('index.html', user=user, playlists=playlists)
    else:
        return render_template('index.html')

@app.route('/username', methods=['GET', 'POST'])
def username():
    form = UsernameForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect('/index')
    return render_template('username.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/collage_details/<playlist_id>', methods=['GET', 'POST'])
def collage_details(playlist_id):
    form = CollageForm()
    if form.validate_on_submit():
        return redirect('/index')
    username = session['username']
    tracks = get_tracks(username, playlist_id)
    num_tracks = len(tracks)
    playlist = get_playlist(playlist_id)
    return render_template('collage_details.html', playlist=playlist, tracks=tracks, num_tracks=num_tracks, form=form)
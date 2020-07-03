from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import UsernameForm, CollageForm
from auth import show_playlists, get_tracks, get_playlist, make_collage, serve_image

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
        print(form)
        session.pop('collage_constants', None)
        session['collage_constants'] = (form.artwork_row.data,int(form.artwork_width.data))
        return redirect('/collage')
    username = session['username']
    tracks = get_tracks(username, playlist_id)
    session.pop('artworks', None)
    num_tracks = len(tracks)
    size = (0, 640)
    if num_tracks > 144:
        size = (2, 64)
    elif num_tracks > 24:
        size = (1, 300)
    artworks = []
    for track in tracks:
        artworks.append(track['track']['album']['images'][size[0]]['url'])
    artworks = list(dict.fromkeys(artworks))
    session['artworks'] = artworks
    playlist = get_playlist(playlist_id)
    return render_template('collage_details.html', playlist=playlist, tracks=tracks, num_tracks=num_tracks, form=form, size=size)

@app.route('/collage')
def collage():
    artworks = session['artworks']
    consts = session['collage_constants']
    print(consts)
    img = make_collage(artworks,consts[0],consts[1])
    return serve_image(img)
    #return render_template('collage.html')
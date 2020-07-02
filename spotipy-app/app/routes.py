from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import UsernameForm
from auth import show_playlists

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
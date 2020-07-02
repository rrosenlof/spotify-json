from app import app
from flask import render_template, flash, redirect
from app.forms import UsernameForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'ross.rosenlof'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/username', methods=['GET', 'POST'])
def username():
   form = UsernameForm()
   if form.validate_on_submit():
       flash('username: {}'.format(form.username.data))
       return redirect('/index')
   return render_template('username.html', title='Sign In', form=form)
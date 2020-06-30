import flask
from flask import request, jsonify, flash, render_template
from auth import show_playlists
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class UsernameForm(Form):
    username = TextField('Username: ', validators=[validators.required()])

    @app.route('/',methods=['GET', 'POST'])
    def home():
        form = UsernameForm(request.form)

        print (form.errors)
        if request.method == 'POST':
            username=request.form['username']
            print (username)
        
        

        return render_template('form.html')   


# https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
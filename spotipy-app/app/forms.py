from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CollageForm(FlaskForm):
    artwork_width = HiddenField()
    artwork_row = IntegerField('Artworks per Row', validators=[DataRequired()])
    submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class UsernameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CollageForm(FlaskForm):
    artwork_width = IntegerField('Artwork Width', validators=[DataRequired()])
    artwork_height = IntegerField('Artwork Height', validators=[DataRequired()])
    artwork_row = IntegerField('Artworks per Row', validators=[DataRequired()])
    submit = SubmitField('Submit')
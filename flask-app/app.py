import flask
from auth import show_playlists
from forms import UsernameForm

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/',methods=['GET', 'POST'])
def home():
    form = UsernameForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('index.html', form=form)


# https://stackoverflow.com/questions/12277933/send-data-from-a-textbox-into-flask
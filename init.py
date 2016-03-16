#module that contains app object and other similar globals

import flask
import flask_sqlalchemy

app = flask.Flask(__name__)
app.config.from_pyfile('settings.py')
db = flask_sqlalchemy.SQLAlchemy(app)
from init import app, db
import flask
import models

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/profile/')
def profile():
    return flask.render_template('profile.html')

@app.route('/lost/')
def lost():
    return flask.render_template('lost.html')

@app.route('/found/')
def found():
    return flask.render_template('found.html')

@app.route('/searchFound/')
def searchFound():
    name = flask.request.args['name']
    #search the database
    return flask.redirect(flask.url_for('found'), code=303)

@app.route('/searchLost/')
def searchLost():
    name = flask.request.args['name']
    # search the database
    return flask.redirect(flask.url_for('lost'), code=303)
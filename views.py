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
    lostPostings = models.LostPosting.query.all()
    return flask.render_template('lost.html', lostPostings=lostPostings)

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

@app.route('/lost/post', methods=['POST'])
def add_post():
    name = flask.request.form['name']
    description = flask.request.form['description']

    #create a new post
    posting = models.LostPosting()

    #set its properties
    posting.name = name
    posting.description = description

    #add it to the database
    db.session.add(posting)

    db.session.commit()
    return flask.redirect(flask.url_for('lost'), code=303)
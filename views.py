from init import app, db
import flask
import models

@app.before_request
def setup_user():
    if 'auth_user' in flask.session:
        user = models.User.query.get(flask.session['auth_user'])
        #save the user in flask., which is a set of globals for this request
        flask.g.user = user
@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/profile/<name>')
def profile(name):
    #pass in id to personalize user
    user = models.User.query.filter_by(login=name).first()
    if user is None:
        flask.abort(404)

    return flask.render_template('profile.html', user=user)

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

@app.route('/login')
def login_form():
    return flask.render_template('login.html')

@app.route('/login', methods=['POST'])
def handle_login():
    login = flask.request.form['user']
    password = flask.request.form['password']
    user = models.User.query.filter_by(login=login).first()
    if user is not None:
        #change this to encrypting password
        if password== user.password:
            flask.session['auth_user'] = user.id
            return flask.redirect(flask.url_for('profile', name=user.login), code=303)

    return flask.render_template('login.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    login = flask.request.form['user']
    password = flask.request.form['password']

    if password != flask.request.form['confirm']:
        # add states to say bad password match
        print("Not a match")

    #check if login is not longer
    if len(login)> 20:
        # add states to say invalid user name
        print("Too long of a username")

    existing = models.User.query.filter_by(login=login).first()

    if existing is not None:
        #return user already exists
        print("soz, this exists")

    user = models.User()
    user.login = login

    #change password to some hash kind
    user.password = password
    print('here')
    db.session.add(user)
    print('here2')
    db.session.commit()
    print('here3')
    flask.session['auth_user'] = user.id

    return flask.redirect(flask.url_for('profile', name=user.login), code=303)
# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template,redirect
from flask import request,session,url_for
#from flask_pymongo import PyMongo
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# import os
# -- Initialization section --
app = Flask(__name__)

# events = [
#         {"event":"First Day of Classes", "date":"2019-08-21"},
#         {"event":"Winter Break", "date":"2019-12-20"},
#         {"event":"Finals Begin", "date":"2019-12-01"}
#     ]

# name of database
app.config['MONGO_DBNAME'] = 'Owelahs_App'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://OwelahsAppAdmin:tJEfOjUk2wGOOa5Y@cluster0.by8nn.mongodb.net/Owlelahs_App?retryWrites=true&w=majority'

mongo = PyMongo(app)

app.secret_key= '?t?~?h??+???v'
# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    # session['username'] = 'Jeffrey' # must be in a route

    #connect to db
    collection=mongo.db.events
    #find all data
    events = collection.find({})

    #return a message
    return render_template('index.html',events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # conect to the database
    events= mongo.db.events
    # insert new data
    events.insert({"event":"Run DMC","date":"01-23-86"})
    # return a message to the user
    return "Event added"

#user to add a new event

@app.route('/events/new', methods=['GET','POST'])

def new_event():
    if request.method == "GET":
        return render_template("new_event.html")
    else:
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        user_name = request.form["user_name"]
        event_desc = request.form["event_desc"]
        # profile_image= request.files["profile_image"]
        # mongo.save_file(profile_image.filename,profile_image)
       

        #connect to db
        collection = mongo.db.events
        #Insert new data
        collection.insert({"event":event_name,"date":event_date,"description":event_desc,"user":user_name})
        #return
        return redirect('/')




@app.route('/name/<name>')

def name(name):
    #connect to db
    collection=mongo.db.events
    #find all data
    events = collection.find({"user":name})

    #return a message
    return render_template('person.html',events = events)

@app.route('/event/<eventID>')

def event(eventID):
    #connect to db
    collection=mongo.db.events
    #find all data
    event = collection.find_one({"_id":ObjectId(eventID)})

    #return a message
    return render_template('event.html',event = event)

#sign up

@app.route('/signup', methods=['POST','GET'])

def signup():
    if request.method== 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name':request.form['username']})

        if existing_user is None:
            users.insert({'name': request.form['username'], 'password': request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'That username alredy exist brother'

    return render_template('signup.html')

#login

@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user: #if there is an anctual login user 
        if request.form['password'] == login_user['password']:#check to see if the password entered is in the database
            session['username'] = request.form['username']#then henerate the session that matches the data base and info entered
            return redirect(url_for('index'))

    return 'Invalid username/password combination'
#both pass and username should match the infor in the data base

#logout

@app.route('/logout')

def logout():
    session.clear()
    return redirect('/')


#only shows my events

@app.route('/myevents')

def myevents():
    #connect to db
    collection=mongo.db.events
    #find all data
    name = session['username']
    events = collection.find({"user":name})

    #return a message
    return render_template('person.html',events = events)
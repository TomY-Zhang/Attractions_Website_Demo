import os
import requests

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#Create routes for all HTML pages
@app.route("/")
def firstpage():
    return render_template("login.html")

@app.route("/signout")
def signout():
    return render_template("login.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@socketio.on("regData")
def regData(data):
    #Get registration info
    reg_email = data["email"]
    reg_user = data["username"]
    reg_pass = data["password"]
    print(reg_email, reg_user, reg_pass)

    #Check if username is already in database
    condition = False
    try:
        credentials = db.execute("SELECT * FROM users WHERE username = :username", {"username": reg_user}).fetchall()[0]
        email, username, password = credentials[0], credentials[1], credentials[2]
        emit("regErrorUser")
    except IndexError:
        #Pass through username test
        condition = True
        pass

    #Check if email is already in database
    try:
        credentials = db.execute("SELECT * FROM users WHERE email = :email", {"email": reg_email}).fetchall()[0]
        email, username, password = credentials[0], credentials[1], credentials[2]
        emit("regErrorEmail")
    except IndexError:
        if condition == True:

            #Put the info into the database
            db.execute("INSERT INTO users (email, username, password) VALUES (:email, :username, :password)", {"email": reg_email, "username": reg_user, "password": reg_pass})
            print(f"{reg_email}, {reg_user}, and {reg_pass} have been inserted into database.")

            emit("regSuccess")
            print("Succesfully emitted!")

    db.commit()

@socketio.on("checkCredentials")
def checkCredentials(data):
    #Get Login Credentials from HTML file
    log_user = data["username"]
    log_pass = data["password"]

    #Define a function to check if user entered anything
    def checkNone(key):
        if key == None:
            emit("loginError")

    checkNone(log_user)
    checkNone(log_pass)

    print(f"Server-side: {log_user}, {log_pass}")

    #Compare login credentials to the ones in the database
    try:
        credentials = db.execute("SELECT * FROM users WHERE username = :username", {"username": log_user}).fetchall()[0]
        print(credentials)

        email, username, password = credentials[0], credentials[1], credentials[2]

        if password == log_pass:
            emit("loginSuccess")
        else:
            emit("loginError")
    except IndexError:
        #If credentials are not found in the database, return an error
        emit("loginError")

@app.route("/explore")
def explore():
    return render_template("explore.html")

#Load comments as soon as the page loads
@app.route("/greatwall")
def greatwall():
    return render_template("greatwall.html")

@app.route("/christ")
def christ():
    return render_template("christ.html")

@app.route("/machupicchu")
def machupicchu():
    return render_template("machupicchu.html")

@app.route("/chichenitza")
def chichenitza():
    return render_template("chichenitza.html")

@app.route("/colosseum")
def colosseum():
    return render_template("colosseum.html")

@app.route("/tajmahal")
def tajmahal():
    return render_template("tajmahal.html")

@app.route("/petra")
def petra():
    return render_template("petra.html")

#Load comments from database when page loads
@socketio.on("gwPageLoaded")
def gw_page_loaded():
    #Get comments from database
    tuple_comments = db.execute("SELECT * FROM gwcomments").fetchall()
    print(tuple_comments)

    #Convert tuple to list
    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)

    #Send data to all clients
    emit("gwLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

#Load comments from database when page loads
@socketio.on("christPageLoaded")
def christ_page_loaded():
    tuple_comments = db.execute("SELECT * FROM christcomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("christLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

#Load comments from database when page loads
@socketio.on("mpPageLoaded")
def mp_page_loaded():
    tuple_comments = db.execute("SELECT * FROM mpcomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("mpLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

#Load comments from database when page loads
@socketio.on("ciPageLoaded")
def ci_page_loaded():
    tuple_comments = db.execute("SELECT * FROM cicomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("ciLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

#Load comments from database when page loads
@socketio.on("rmPageLoaded")
def rm_page_loaded():
    tuple_comments = db.execute("SELECT * FROM rmcomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("rmLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

@socketio.on("tmPageLoaded")
def tm_page_loaded():
    tuple_comments = db.execute("SELECT * FROM tmcomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("tmLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

@socketio.on("petraPageLoaded")
def petra_page_loaded():
    tuple_comments = db.execute("SELECT * FROM petracomments").fetchall()
    print(tuple_comments)

    list_comments = [x[0] for x in tuple_comments]
    print(list_comments)
    emit("petraLoadComments", {"comments": list_comments}, broadcast = True)

    db.commit()

#Get message from client
@socketio.on("gwComment")
def gw_comment(data):
    #Get comment from client
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    #Insert comment into database to make it permanent
    db.execute("INSERT INTO gwcomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    #Send the message to all clients
    emit("gwCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("christComment")
def christ_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO christcomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("christCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("mpComment")
def mp_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO mpcomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("mpCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("ciComment")
def ci_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO cicomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("ciCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("rmComment")
def rm_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO rmcomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("rmCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("tmComment")
def tm_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO tmcomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("tmCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()

@socketio.on("petraComment")
def petra_comment(data):
    comment = data["comment"]
    print(f"Server successfully recieved {comment}")

    db.execute("INSERT INTO petracomments (comments) VALUES (:comment)", {"comment": comment})
    print("Comment succesfully put into database!")

    emit("petraCommentAll", {"comment": comment}, broadcast = True)
    print("Comment succesfully emitted to all clients!")

    db.commit()
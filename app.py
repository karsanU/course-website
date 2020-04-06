from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import *
from databaseSchema import *


# Initialize app
app = Flask(__name__)
engine = create_engine('sqlite:///assignment3.db', echo=True)
s = scoped_session(sessionmaker(bind=engine))
 

@app.teardown_request
def remove_session(ex=None):
    s.remove()


@app.route('/')
def prompt():
    if not session.get("logged_in"):
        return render_template("login.html")
    else:
        return home()

@app.route('/loginPage')
def loginPage():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    # Initialize database
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    query = s.query(User).filter(User.username.in_(
        [POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()


    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return prompt()


@app.route("/signUpPage")
def signUpPage():
    allInstructors = s.query(Instructor)
    allStudents = s.query(Student)
    return render_template("signUp.html", allStudents=allStudents, allInstructors=allInstructors)

@app.route("/signUp",methods=['POST'] )
def signUp():
    pass




@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/news')
def news():
    return render_template("news.html")


@app.route('/lectures')
def lectures():
    return render_template("lectures.html")


@app.route('/labs')
def labs():
    return render_template("labs.html")


@app.route('/contacts')
def contact():
    return render_template("contacts.html")


@app.route('/assignments')
def assignments():
    return render_template("assignments.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return prompt()


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)

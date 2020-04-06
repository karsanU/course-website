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
# store all usernames globally for future purpose


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
        flash('wrong username or passwrod')
    return prompt()


@app.route("/signUpPage")
def signUpPage():
    allInstructors = s.query(Instructor)
    allStudents = s.query(Student)

    return render_template("signUp.html", allStudents=allStudents, allInstructors=allInstructors)


@app.route("/signUp", methods=['POST'])
def signUp():
    allUsers = s.query(User)
    usernameList = []
    for u in allUsers:
        usernameList.append(u.username)
    if (str(request.form['username']) in usernameList):
        flash("Username: " +
              str(request.form['username']) + ", is already in use.")
        return signUpPage()

    # push new user to the database
    username = str(request.form['username'])
    password = str(request.form['password1'])
    firstName = str(request.form['firstName'])
    lastName = str(request.form['lastName'])
    accType = request.form.get('selectAccType')
    selectStudents = request.form.getlist('selectStudents')
    selectInstructors = request.form.getlist('selectInstructors')

    # new user is a student
    if accType == "student":
        # add the student and use associated tables to database
        ####
        newUser = User(username=username, password=password,
                       isInstructor=False)
        s.add(newUser)
        s.commit()
        ####
        newStudent = Student(userId=newUser.id, username=username,
                             firstName=firstName, lastName=lastName)
        s.add(newStudent)
        s.commit()
        ####
        newGrade = Grades(studentId=newStudent.id)
        s.add(newGrade)
        s.commit()

        # add student's instructors
        for iUsername in selectInstructors:
            instructorObj = s.query(Instructor).filter_by(
                username=iUsername).first()
            newStudent.instructor.append(instructorObj)
            s.commit()
        flash("New account created for: " +
              newStudent.firstName + " " + newStudent.lastName)

    # new user is a instructor
    else:
        # add the user and use associated tables to database
        ####
        newUser = User(username=username, password=password, isInstructor=True)
        s.add(newUser)
        s.commit()
        ####
        newInstructor = Instructor(
            userId=newUser.id, username=username, firstName=firstName, lastName=lastName)
        s.add(newInstructor)
        s.commit()

        # add student's instructors
        for sUsername in selectInstructors:
            studentObj = s.query(Student).filter_by(username=sUsername).first()
            newInstructor.student.append(studentObj)
            s.commit()
        flash("New account created, welcome " +
              newInstructor.firstName + " " + newInstructor.lastName)

    return home()


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

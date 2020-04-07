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
# current user;


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
    # set current global user
    if result:
        session['logged_in'] = True
        session['user'] = POST_USERNAME
        if ((s.query(User).filter_by(username=POST_USERNAME).first()).isInstructor) == 0:
            session['accountType'] = "student"
        else:
            session['accountType'] = "instructor"

    else:
        flash('wrong username or password')
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
                       isInstructor=0)
        s.add(newUser)
        s.commit()
        session['logged_in'] = True
        session['user'] = newUser.username
        session['accountType'] = "student"
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
        newUser = User(username=username, password=password, isInstructor=1)
        s.add(newUser)
        s.commit()
        session['logged_in'] = True
        session['user'] = newUser.username
        session['accountType'] = "instructor"

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


@app.route('/viewGrades')
def viewGrades():
    if session.get("logged_in") == False:
        return logout()
    return render_template("gradesStudent.html", user=s.query(User).filter_by(username=session.get("user")).first(), accType=session.get("accountType"))


@app.route('/processRemarkRequest', methods=['POST'])
def processRemarkRequest():
    student = s.query(Student).filter_by(username=session.get("user")).first()
    remarkMessage = str(request.form['remarkMessage'])
    if 'a1' in request.form:
        student.grades.a1remark =1
        student.grades.a1remarkMessage = remarkMessage
    elif 'a2' in request.form:
        student.grades.a2remark =1
        student.grades.a2remarkMessage = remarkMessage
    elif 'a3' in request.form:
        student.grades.a3remark =1
        student.grades.a3remarkMessage = remarkMessage
    elif 'labs' in request.form:
        student.grades.labsRemark =1
        student.grades.labsRemarkMessage = remarkMessage
    elif 'midterm' in request.form:
        student.grades.midtermRemark =1
        student.grades.midtermRemarkMessage = remarkMessage
    elif 'final' in request.form: 
        student.grades.finalRemark =1
        student.grades.midtermRemarkMessage = remarkMessage
    s.commit()
    return render_template("gradesStudent.html", user=s.query(User).filter_by(username=session.get("user")).first(), accType=session.get("accountType"))


@app.route('/home')
def home():
    if session.get("logged_in") == False:
        return logout()
    acctype = "instructor"
    return render_template("index.html", accType=session.get("accountType"))


@app.route('/news')
def news():
    if session.get("logged_in") == False:
        return logout()
    return render_template("news.html", accType=session.get("accountType"))


@app.route('/lectures')
def lectures():
    if session.get("logged_in") == False:
        return logout()
    return render_template("lectures.html", accType=session.get("accountType"))


@app.route('/labs')
def labs():
    if session.get("logged_in") == False:
        return logout()
    return render_template("labs.html", accType=session.get("accountType"))


@app.route('/contacts')
def contact():
    if session.get("logged_in") == False:
        return logout()
    return render_template("contacts.html", accType=session.get("accountType"))


@app.route('/assignments')
def assignments():
    if session.get("logged_in") == False:
        return logout()
    return render_template("assignments.html", accType=session.get("accountType"))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['user'] = None
    session['accountType'] = None
    return prompt()


if __name__ == '__main__':
    app.secret_key = 'super456secret&*)(key'
    app.run(debug=True)

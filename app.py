from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
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
        return redirect(url_for('loginPage'))
    else:
        return redirect(url_for('home'))


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
        session['userName'] = POST_USERNAME
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
        session['userName'] = newUser.username
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
        session['userName'] = newUser.username
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

    return redirect(url_for('home'))

@app.route('/viewGrades')
def viewGrades():
    if session.get("logged_in") == False:
        return logout()
    return render_template("gradesStudent.html", user=s.query(User).filter_by(username=session.get("userName")).first(), accType=session.get("accountType"))


@app.route('/processRemarkRequest', methods=['POST'])
def processRemarkRequest():
    student = s.query(Student).filter_by(username=session.get("userName")).first()
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
        student.grades.finalRemarkMessage = remarkMessage
    s.commit()
    return redirect(url_for('viewGrades'))

@app.route('/showMyStudents')
def showMyStudents():
    myStudents = s.query(Instructor).filter_by(username=session.get("userName")).first().student
    return render_template("showMyStudents.html", myStudents =myStudents, accType=session.get("accountType"))

@app.route('/redirect-editStudentGrade',  methods=['POST'])
def redirecteditStudentGrade():
    for key in request.form.keys():
        studentUsername = key
    session['studentBeingViewed'] = studentUsername
    return redirect(url_for('editStudentGrade'))

@app.route('/remarkRequests', )
def RemarkRequests():
    remarkStudents=[]
    myStudents = s.query(Instructor).filter_by(username=session.get("userName")).first().student
    for student in  myStudents: 
        grades = student.grades
        if(grades.a1remark == 1 or grades.a2remark == 1 or grades.a3remark == 1 or 
        grades.labsRemark == 1 or grades.midtermRemark == 1 or grades.finalRemark == 1 ):
            remarkStudents.append(student)
    return render_template("remarkRequests.html", remarkStudents =remarkStudents, accType=session.get("accountType"))

@app.route('/editStudentGrade', )
def editStudentGrade():
    studentUsername = session.get("studentBeingViewed")
    student=s.query(Student).filter_by(username=studentUsername).first()
    return render_template("editStudentGrade.html", student =student, accType=session.get("accountType"))

@app.route('/modifyGrade',  methods=['POST'])
def modifyGrade():
    studentUsername = session.get("studentBeingViewed")
    student=s.query(Student).filter_by(username=studentUsername).first()
    if 'a1' in request.form:
        student.grades.a1 = int(request.form['newMark'])
        student.grades.a1remark =0
        student.grades.a1remarkMessage = None
    elif 'a2' in request.form:
        student.grades.a2 = int(request.form['newMark'])
        student.grades.a2remark =0
        student.grades.a2remarkMessage = None
    elif 'a3' in request.form:
        student.grades.a3 = int(request.form['newMark'])
        student.grades.a3remark =0
        student.grades.a3remarkMessage = None
    elif 'labs' in request.form:
        student.grades.labs = int(request.form['newMark'])
        student.grades.labsRemark =0
        student.grades.labsRemarkMessage = None
    elif 'midterm' in request.form:
        student.grades.midterm = int(request.form['newMark'])
        student.grades.midtermRemark =0
        student.grades.midtermRemarkMessage = None
    elif 'final' in request.form: 
        student.grades.final = int(request.form['newMark'])
        student.grades.finalRemark =0
        student.grades.finalRemarkMessage = None
    s.commit()
    return render_template("editStudentGrade.html", student =student, accType=session.get("accountType"))


@app.route('/giveFeedback')
def giveFeedback():
    if session.get("logged_in") == False:
        return logout()
        
    instructors = s.query(Student).filter_by(username=session.get("userName")).first().instructor
    return render_template("giveFeedback.html", accType=session.get("accountType"), instructors=instructors)

@app.route('/giveFeedbackProcess',  methods=['POST'])
def giveFeedbackProcess():
    if session.get("logged_in") == False:
        return logout()
    q1 = str(request.form['q1'])
    q2 = str(request.form['q2'])
    q3 = str(request.form['q3'])
    q4 = str(request.form['q4'])
    instructorUsername = request.form.get('listInstructors')
    instructor = s.query(Instructor).filter_by(username=instructorUsername).first()
    feedback = Feedback(instructorId=instructor.id, q1=q1, q2=q2, q3=q3, q4=q4)
    s.add(feedback)
    s.commit()
    return redirect(url_for('giveFeedback'))
    
@app.route('/viewFeedback')
def viewFeedback():
    if session.get("logged_in") == False:
        return logout()
    feedback = s.query(Instructor).filter_by(username=session.get("userName")).first().feedbacks
    return render_template("viewFeedback.html", accType=session.get("accountType"), feedback=feedback)


@app.route('/home')
def home():
    if session.get("logged_in") == False:
        return logout()
    # send who is logged in
    user = s.query(User).filter_by(username=session.get("userName")).first()
    if user.isInstructor == True:
        user = user.instructor
    else:
        user = user.student
    return render_template("index.html", accType=session.get("accountType"), user=user)


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
    session['userName'] = None
    session['accountType'] = None
    return redirect(url_for('loginPage'))


if __name__ == '__main__':
    app.secret_key = 'super456secret&*)(key'
    app.run(debug=True)

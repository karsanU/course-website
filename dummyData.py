import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSchema import *

engine = create_engine('sqlite:///assignment3.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()



# add user
instructor1 = User(username="instructor1",password="instructor1",isInstructor=True)
session.add(instructor1)

instructor2 = User(username="instructor2",password="instructor2",isInstructor=True)
session.add(instructor2)

student1User = User(username="student1",password="student1",isInstructor=False)
session.add(student1User)

student2User = User(username="student2",password="student2",isInstructor=False)
session.add(student2User)
session.commit()


# add instructor 
bobTeach = Instructor(userId=instructor1.id, username=instructor1.username,  firstName='Bob', lastName='Lucio')
session.add(bobTeach)

stevenTeach = Instructor(userId=instructor2.id, username=instructor2.username, firstName='Steven', lastName='Xaio')
session.add(stevenTeach)
session.commit()

# add student 
karsanStudent = Student(userId=student1User.id, username=student1User.username, instructorId = bobTeach.id, firstName='Karsan', lastName='Uthayakumar')
session.add(karsanStudent)

hamishStudent= Student(userId=student2User.id, username=student2User.username, instructorId = stevenTeach.id, firstName='Hamsih', lastName='Rajiv')
session.add(hamishStudent)
session.commit()

# add grades
karsanGrade = Grades(studentId = karsanStudent.id, a1=99, a2 = 100, a3=99, midterm=99, final=100, remark=True)
session.add(karsanGrade)   

hamsihGrade = Grades(studentId = hamishStudent.id, a1=99, a2 = 100, a3=99, midterm=99, final=100, remark=False)
session.add(hamsihGrade)
session.commit()

# add feedback 
feedback1 = Feedback(instructorId=bobTeach.id, studentId=karsanStudent.id, q1="Please bring donuts for all students.", q2="",q3="", q4="")
session.add(feedback1)

feedback2 = Feedback(instructorId=stevenTeach.id, studentId=hamishStudent.id, q1="Please bring cookies for all students.", q2="",q3="", q4="")
session.add(feedback2)
session.commit()

# commit the record the database 
session.commit()


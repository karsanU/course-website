from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Table, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///assignment3.db', echo=True)
Base = declarative_base()

#######################################################
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    isInstructor = (Boolean) 
    instructor = relationship("Instructor", uselist=False, back_populates="user")
    student = relationship("Student", uselist=False, back_populates="user")

class Instructor(Base):
    __tablename__ = "instructor"
    id = Column(Integer, primary_key=True)
    userid = Column(String, ForeignKey('user.id'), unique=True)
    username = Column(String, unique=True)
    firstname = Column(String)
    lastname = Column(String)
    user = relationship("User", back_populates="instructor")
    students = relationship("Student")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer,  ForeignKey('user.id'))
    username = Column(String, unique=True)
    instructorid = Column(String, ForeignKey('instructor.userid'), unique=True)
    firstname = Column(String)
    lastname = Column(String)
    user = relationship("User", back_populates="student")

    

'''

 


    # parent of grades   
    #grades = relationship('Grades', uselist=False, back_populates="parent")

    def __init__(self, userId, username, firstname, lastname, teacherId):
        self.userId = userId
        self.username = username
        self.firstname = firstname
        self.lastname = lastname 
        self.teacherId = teacherId
     
class Grades(Base):
    __tablename__ = "grades"
    studentId = Column(Integer,  ForeignKey('student.userId'), primary_key=True)
    a1 = Column(Integer)
    a2 = Column(Integer)
    a3 = Column(Integer)
    midterm =  Column(Integer)
    final =  Column(Integer)
    remark = Column(Boolean)
    #child of student, 1-1
    #student = relationship("Student", back_populates="child")

    def __init__(self, a1, a2, a3,midterm,final):
        self.studentId = studentId
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3 
        self.midterm = midterm 
        self.final = final

class Feedback(Base):
    __tablename__ = "feedback"
    teacher_id = Column(Integer,  ForeignKey('teacher.userId'), primary_key=True)
    student_id = Column(Integer,  ForeignKey('student.id'), primary_key=True)
    feedback = Column(String)

    def __init__(self, teacher_id, student_id, feedback):
        self.teacher_id = teacher_id
        self.student_id = student_id
        self.feedback = feedback 
 
'''

# create tables'

Base.metadata.create_all(engine)


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

    #student = relationship("Student", uselist=False, back_populates="user")
 

class Instructor(Base):
    __tablename__ = "instructor"
    id = Column(Integer, primary_key=True, unique=True)
    userId = Column(String, ForeignKey('user.id'))
    username = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    user = relationship("User", back_populates="instructor")
    students = relationship("Student")
    feedbacks = relationship("Feedback")



class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer,  ForeignKey('user.id'))
    username = Column(String, unique=True)
    instructorId = Column(String, ForeignKey('instructor.userId'), unique=True)
    firstName = Column(String)
    lastName = Column(String)
    #user = relationship("User", back_populates="student")
    grades = relationship("Grades", uselist=False, back_populates="student")


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    studentId = Column(Integer,  ForeignKey('student.id'))
    a1 = Column(Integer)
    a2 = Column(Integer)
    a3 = Column(Integer)
    midterm = Column(Integer)
    final = Column(Integer)
    remark = Column(Boolean)
    remarkMessage = Column(String)
    student = relationship("Student", back_populates="grades")

class Feedback(Base):
    __tablename__ = "feedback"
    instructorId = Column(Integer,  ForeignKey('instructor.id'), primary_key=True)
    studentId = Column(Integer,  ForeignKey('student.id'), primary_key=True)
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)
    q4 = Column(String)

# create tables'
Base.metadata.create_all(engine)


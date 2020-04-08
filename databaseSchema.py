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
    isInstructor = Column(Integer) 
    instructor = relationship("Instructor", uselist=False, back_populates="user")
    student = relationship("Student", uselist=False, back_populates="user")
 

association_table = Table('association', Base.metadata,
    Column('instructorId', Integer, ForeignKey('instructor.id')),
    Column('studentId', Integer, ForeignKey('student.id'))
) 

class Instructor(Base):
    __tablename__ = "instructor"
    id = Column(Integer, primary_key=True, unique=True)
    userId = Column(String, ForeignKey('user.id'))
    username = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    user = relationship("User", back_populates="instructor")
    student = relationship(
        "Student",
        secondary=association_table,
        back_populates="instructor")
    feedbacks = relationship("Feedback")



class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    userId = Column(Integer,  ForeignKey('user.id'))
    username = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    instructor = relationship(
        "Instructor",
        secondary=association_table,
        back_populates="student")
    user = relationship("User", back_populates="student")
    grades = relationship("Grades", uselist=False, back_populates="student")


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    studentId = Column(Integer,  ForeignKey('student.id'))
    a1 = Column(Integer)
    a1remark = Column(Integer, default = 0)
    a1remarkMessage = Column(String, default = None)
    a2 = Column(Integer)
    a2remark = Column(Integer, default = 0)
    a2remarkMessage = Column(String, default = None)
    a3 = Column(Integer)
    a3remark = Column(Integer, default = 0)
    a3remarkMessage = Column(String, default = None)
    labs = Column(Integer)
    labsRemark = Column(Integer, default = 0)
    labsRemarkMessage = Column(String, default = None)
    midterm = Column(Integer)
    midtermRemark = Column(Integer, default = 0)
    midtermRemarkMessage = Column(String, default = None)
    final = Column(Integer)
    finalRemark = Column(Integer, default = 0)
    finalRemarkMessage = Column(String, default = None) 
    student = relationship("Student", back_populates="grades")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    instructorId = Column(Integer,  ForeignKey('instructor.id'))
    q1 = Column(String)
    q2 = Column(String)
    q3 = Column(String)
    q4 = Column(String)

# create tables'
Base.metadata.create_all(engine)


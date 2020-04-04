import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

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

teacher1 = Instructor(userid=instructor1.id, username=instructor1.username,  firstname='Bob', lastname='Lucio')
session.add(teacher1)

teacher2 = Instructor(userid=instructor2.id, username=instructor2.username, firstname='Steven', lastname='Xaio')
session.add(teacher2)

'''
# add teacher 


# add student 
student1 = Student(id=student1User.id, username=student1User.username, teacher_id = instructor1.id, firstname='Karsan', lastname='Uthayakumar')
session.add(student1)

student2 = Student(id=student2User.id, username=student2User.username, teacher_id = instructor2.id, firstname='Hamsih', lastname='Rajiv')
session.add(student2)
'''


# commit the record the database 
session.commit()


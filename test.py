import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSchema import *

engine = create_engine('sqlite:///assignment3.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
s = Session()

students = s.query(Student)

for s in students:
    for i in s.instructor:
        print(i.student[0].firstName)
    print ("----------")




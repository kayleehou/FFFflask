""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class post(db.Model):
    __tablename__ = 'class'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('class.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, note, image):
        self.userID = id
        self.note = note
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            "base64": str(file_encode)
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _date = db.Column(db.String(255), unique=False, nullable=False)
    _time = db.Column(db.String(255), unique=True, nullable=False)
    _location = db.Column(db.String(255), unique=True, nullable=False)
    _nameOfClass = db.Column(db.String(255), unique=True, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, date, time, location, nameOfClass):
        self._date = date    # variables with self prefix become part of the object, 
        self._time = time
        self._location = location
        self._nameOfClass = nameOfClass

    # a name getter method, extracts name from object
    @property
    def date(self):
        return self._date
    
    # a setter function, allows name to be updated after initial object creation
    @date.setter
    def date(self, date):
        self._date = date

    # a name getter method, extracts name from object
    @property
    def time(self):
        return self._time
    
    # a setter function, allows name to be updated after initial object creation
    @time.setter
    def time(self, time):
        self._time = time
    
    # a getter method, extracts email from object
    @property
    def location(self):
        return self._location
    
    # a setter function, allows name to be updated after initial object creation
    @location.setter
    def location(self, location):
        self._location = location
        
        # a name getter method, extracts name from object
    @property
    def nameOfClass(self):
        return self._nameOfClass
    
    # a setter function, allows name to be updated after initial object creation
    @nameOfClass.setter
    def nameOfClass(self, nameOfClass):
        self._nameOfClass = nameOfClass
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "nameOfClass": self.nameOfClass,
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, date="", time="", location="", nameOfClass=""):
        """only updates values with length"""
        if len(date) > 0:
            self.date = date
        if len(time) > 0:
            self.time = time
        if len(location) > 0:
            self.location = location
        if len(nameOfClass) > 0:
            self.nameOfClass = nameOfClass
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(date='2/23/23', time='10:00', location='4s Ranch', classname='Small Dogs')
    u2 = User(date='2/24/23', time='12:00', location='San Diego', classname='Medium Dogs')
    u3 = User(date='2/25/23', time='8:00', location='Poway', classname='Big Dogs')
    u4 = User(date='2/26/23', time='11:00', location='Los Angeles', classname='Large Dogs')

    users = [u1, u2, u3, u4]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.date + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.date}")
            
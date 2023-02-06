""" database dependencies to support sqliteDB examples """
from random import randrange
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from datetime import date


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(dog, id, note, image):
        dog.userID = id
        dog.note = note
        dog.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(dog):
        return "Notes(" + str(dog.id) + "," + dog.note + "," + str(dog.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(dog):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(dog)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return dog
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(dog):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, dog.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
        file_encode = base64.encodebytes(file_read)
        
        return {
            "id": dog.id,
            "userID": dog.userID,
            "note": dog.note,
            "image": dog.image,
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
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _breed = db.Column(db.String(255), unique=False, nullable=False)
    _sex = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.String(255), unique=False, nullable=False)
    _price = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (dog)
    def __init__(dog, name, uid, breed, sex, dob, price):
        dog._name = name    # variables with dog prefix become part of the object, 
        dog._uid = uid
        dog._breed = breed
        dog._sex = sex 
        dog._dob = dob
        dog._price = price

    # a name getter method, extracts name from object
    @property
    def name(dog):
        return dog._name
    
    # first name setter 
    @name.setter
    def name(dog, name):
        dog._name = name
    
    # last name getter 
    @property
    def uid(dog):
        return dog._uid
    
    # last name setter 
    @uid.setter
    def uid(dog, uid):
        dog._uid = uid
    
    #breed getter 
    @property
    def breed(dog):
        return dog._breed
    
    #breed setter
    @breed.setter
    def breed(dog, breed):
        dog._breed = breed
    
    #hours per week getter    
    @property
    def sex(dog):
        return dog._sex
    
    # sex setter
    @sex.setter
    def sex(dog, sex):
        dog._sex = sex
        
    #coach name getter    
    @property
    def dob(dog):
        dob_string = dog._dob.strftime('%m-%d-%Y')
        return dob_string
    
    # dob should be have verification for type date
    @dob.setter
    def dob(dog, dob):
        dog._dob = dob

    @property
    def age(dog):
        today = date.today()
        return today.year - dog._dob.year- ((today.month, today.day) < (dog._dob.month, dog._dob.day))
    
    #getter
    @property
    def price(dog):
        return dog._price
    
    #setter
    @price.setter
    def price(dog, price):
        dog._price = price
        
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(dog):
        return json.dumps(dog.read())

    # CRUD create/add a new record to the table
    # returns dog or None on error
    def create(dog):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(dog)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return dog
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts user to dictionary
    # returns dictionary
    def read(dog):
        return {
            "id": dog.id,
            "name": dog.name,
            "uid": dog.uid,
            "breed": dog.breed,
            "sex": dog.sex,
            "dob": dog.dob,
            "price": dog.price,
            "posts": [post.read() for post in dog.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns dog
    def update(dog, name="", uid="", breed="", sex="", dob="", price=""):
        """only updates values with length"""
        if len(name) > 0:
            dog.name = name
        if len(uid) > 0:
            dog.uid = uid
        if len(breed) > 0:
            dog.breed = breed
        if len(sex) > 0:
            dog.sex = sex
        if len(dob) > 0:
            dog.dob = dob
        if len(price) > 0:
            dog.price = price
        db.session.commit()
        return dog

    # CRUD delete: remove dog
    # None
    def delete(dog):
        db.session.delete(dog)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(name='Joe', uid='81729', breed='Labrador Retriever Blend', sex='male', dob=date(2022, 2, 11), price='$200')
    u2 = User(name='Bean', uid='83792', breed='Shepherd-Rottweiler Blend', sex="male", dob=date(2019, 1, 31), price='$180')
    u3 = User(name='Harry', uid='80032', breed='Hound-Terrier Blend', sex= "male", dob=date(2020, 4, 29), price='$160')
    u4 = User(name='Honey', uid='90276', breed='Retriever Blend', sex= "female", dob=date(2021, 11, 1), price='$200')
    u5 = User(name='George', uid='90277', breed='Retriever Blend', sex= "male", dob=date(2021, 11, 1), price='$200')
    u6 = User(name='Julie', uid='91236', breed='Black Mouth Cur Blend', sex= "female", dob=date(2022, 4, 9), price='$250')
    u7 = User(name='Violet', uid='86327', breed='Retriever Blend', sex= "female", dob=date(2021, 6, 5), price='$198')
    u8 = User(name='Doug', uid='87729', breed='Shepherd Blend', sex= "male", dob=date(2018, 11, 1), price='$120')
    u9 = User(name='Thor', uid='90028', breed='Retriever Blend', sex= "male", dob=date(2020, 8, 17), price='$200')
    u10 = User(name='Stark', uid='92888', breed='Doberman Pinscher Blend', sex= "male", dob=date(2020, 9, 12), price='$220')
    u11 = User(name='Bucky', uid='94465', breed='Border Collie-Shepherd Blend', sex= "male", dob=date(2020, 9, 24), price='$140')
    u12 = User(name='Wanda', uid='90992', breed='Shepherd-Husky Blend', sex= "female", dob=date(2019, 2, 1), price='$260')
    u13 = User(name='Tasha', uid='94327', breed='Jack Russel Terrier', sex= "female", dob=date(2019, 10, 20), price='$130')
    u14 = User(name='Shang', uid='80786', breed='Chihuahua Short Coat', sex= "male", dob=date(2019, 8, 25), price='$140')
    u15 = User(name='Parker', uid='86009', breed='Dachshund', sex= "male", dob=date(2020, 3, 9), price='$155')
    u16 = User(name='Cap', uid='89322', breed='Beagle', sex= "male", dob=date(2022, 1, 11), price='$200')
    u17 = User(name='Shuri', uid='85359', breed='American Staffordshire Terrier', sex= "female", dob=date(2022, 1, 23), price='$190')
    u18 = User(name='Musa', uid='96971', breed='American Bulldog', sex= "female", dob=date(2022, 2, 22), price='$160')
    u19 = User(name='Bloom', uid='91298', breed='Maltese', sex= "female", dob=date(2017, 12, 11), price='$110')
    u20 = User(name='Stella', uid='98030', breed='Cattle Dog', sex= "female", dob=date(2017, 12, 27), price='$220')
    

    users = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.name}")
            
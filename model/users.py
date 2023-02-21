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
        # file_encode = base64.encodebytes(file_read)
        
        return {
            "id": self.id,
            "userID": self.userID,
            "note": self.note,
            "image": self.image,
            # "base64": str(file_encode)
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
    _image = db.Column(db.String(255), unique=True, nullable=False)
    _link = db.Column(db.String(255), unique=False, nullable=False)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _breed = db.Column(db.String(255), unique=False, nullable=False)
    _sex = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _price = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (dog)
    def __init__(dog, image, link, name, uid, breed, sex, dob, price):
        dog._image = image
        dog._link = link
        dog._name = name    # variables with dog prefix become part of the object, 
        dog._uid = uid
        dog._breed = breed
        dog._sex = sex 
        dog._dob = dob
        dog._price = price

    @property
    def image(dog):
        return dog._image
    
    # a setter function, allows name to be updated after initial object creation
    @image.setter
    def image(dog, image):
        dog._image = image

    @property
    def link(dog):
        return dog._link
    
    # a setter function, allows name to be updated after initial object creation
    @link.setter
    def link(dog, link):
        dog._link = link
        
    # name GETTER
    @property
    def name(dog):
        return dog._name
    
    # first name setter 
    @name.setter
    def name(dog, name):
        dog._name = name
    
    # last name getter 
    @property
    def breed(dog):
        return dog._breed
    
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
            "image": dog.image,
            "link" : dog.link,
            "name": dog.name,
            "uid": dog.uid,
            "breed": dog.breed,
            "sex": dog.sex,
            "dob": dog.dob,
            "age": dog.age,
            "price": dog.price,
            # "posts": [post.read() for post in dog.posts]
        }

    # CRUD update: updates user name, password, phone
    # returns dog
    def update(dog, image="", link="", name="", uid="", breed="", sex="", dob="", price=""):
        """only updates values with length"""
        if len(image) > 0:
            dog.image = image
        if len(link) > 0:
            dog.link = link   
        if len(name) > 0:
            dog.name = name
        if len(uid) > 0:
            dog.uid = uid
        if len(breed) > 0:
            dog.breed = breed
        if len(sex) > 0:
            dog.sex = sex
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
    with app.app_context():
        """Create database and tables"""
        db.init_app(app)
        db.create_all()
        """Tester data for table"""
    u1 = User('https://do31x39459kz9.cloudfront.net/storage/image/cc7c5dd6a09649e3bf5c6bca96b21daa-1670625496-1670625511-jpg/1024-0-', 'https://haeryny.github.io/teamteam/doginfo/', name='Joe', uid='81729', breed='Labrador Retriever Blend', sex='male', dob=date(2022, 2, 11), price='$200')
    u2 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/672cb9b41e7548f68316d4a328c772d2-1673989499-1673989524-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Bean', uid='83792', breed='Shepherd-Rottweiler Blend', sex="male", dob=date(2019, 1, 31), price='$180')
    u3 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/9f57a9ccb04d489c8e0faeb7a6aaecc1-1671755085-1671755107-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Harry', uid='80032', breed='Hound-Terrier Blend', sex= "male", dob=date(2020, 4, 29), price='$160')
    u4 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/7a0fd8c5107f469a8b6e3ec6db1bc48a-1671827148-1671827194-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Honey', uid='90276', breed='Retriever Blend', sex= "female", dob=date(2021, 11, 1), price='$200')
    u5 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/3b17d9a97b4e41ff984e54467d122820-1670895829-1670895970-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='George', uid='90277', breed='Retriever Blend', sex= "male", dob=date(2021, 11, 1), price='$200')
    u6 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/574b155c13f5453093faa9a9bbe6cc09-1672428396-1672428453-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Julie', uid='91236', breed='Black Mouth Cur Blend', sex= "female", dob=date(2022, 4, 9), price='$250')
    u7 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/286ffc0f2e2f4227b804656084a2eb1c-1675561494-1675561497-jpeg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Violet', uid='86327', breed='Retriever Blend', sex= "female", dob=date(2021, 6, 5), price='$198')
    u8 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/1e445a3de6a44e9ca42ff1f36da4a9b0-1674933023-1674933059-jpeg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Doug', uid='87729', breed='Shepherd Blend', sex= "male", dob=date(2018, 11, 1), price='$120')
    u9 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/7921672da5a745d497b014d1e25802eb-1673041880-1676231549-jpeg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Thor', uid='90028', breed='Retriever Blend', sex= "male", dob=date(2020, 8, 17), price='$200')
    u10 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/16890ba2d55b4d2b99b4c1149f8425c5-1675099945-1675099968-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Stark', uid='92888', breed='Doberman Pinscher Blend', sex= "male", dob=date(2020, 9, 12), price='$220')
    u11 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/da1af9aca3db4c76b250193cafbe6874-1675374061-1675374069-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Bucky', uid='94465', breed='Border Collie-Shepherd Blend', sex= "male", dob=date(2020, 9, 24), price='$140')
    u12 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/3153afbaf9ed464ab7ab05de8cc68245-1660424834-1661448994-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Wanda', uid='90992', breed='Shepherd-Husky Blend', sex= "female", dob=date(2019, 2, 1), price='$260')
    u13 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/0c5b23a621874bbcbb4af72e870f2396-1662938148-1662938165-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Tasha', uid='94327', breed='Jack Russel Terrier', sex= "female", dob=date(2019, 10, 20), price='$130')
    u14 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/d9681fb1d6ec4e718a58a6dd40e4b333-1675210646-1675558115-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Shang', uid='80786', breed='Chihuahua Short Coat', sex= "male", dob=date(2019, 8, 25), price='$140')
    u15 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/7046abe642674a07bb4ff5a8f5c44da0-1675283719-1675283745-jpeg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Parker', uid='86009', breed='Dachshund', sex= "male", dob=date(2020, 3, 9), price='$155')
    u16 = User(image='https://i0.wp.com/timesofsandiego.com/wp-content/uploads/2022/08/Beagle.jpg?ssl=1', link='https://haeryny.github.io/teamteam/doginfo/', name='Cap', uid='89322', breed='Beagle', sex= "male", dob=date(2022, 1, 11), price='$200')
    u17 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/3236e8ede81d4e44b9bf806a18464230-1666577817-1666577841-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Shuri', uid='85359', breed='American Staffordshire Terrier', sex= "female", dob=date(2022, 1, 23), price='$190')
    u18 = User(image='https://do31x39459kz9.cloudfront.net/storage/image/daddeb64a1374a75821e01893d456306-1671391639-1671391712-jpg/1024-0-', link='https://haeryny.github.io/teamteam/doginfo/', name='Musa', uid='96971', breed='American Bulldog', sex= "female", dob=date(2022, 2, 22), price='$160')
    u19 = User(image='https://www.aspcapetinsurance.com/media/2325/facts-about-maltese-dogs.jpg', link='https://haeryny.github.io/teamteam/doginfo/', name='Bloom', uid='91298', breed='Maltese', sex= "female", dob=date(2017, 12, 11), price='$110')
    u20 = User(image='https://dl5zpyw5k3jeb.cloudfront.net/organization-photos/38001/4/?bust=1516228994&width=720', link='https://haeryny.github.io/teamteam/doginfo/', name='Stella', uid='98030', breed='Cattle Dog', sex= "female", dob=date(2017, 12, 27), price='$220')
    

    users = [u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13, u14, u15, u16, u17, u18, u19, u20]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + user.name + " note " + str(num) + ". \n Generated by test data."
                #user.posts.append(Post(id=user.id, note=note, image='ncs_logo.png'))
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.name}")
            
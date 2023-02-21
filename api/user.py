from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User
# import requests  # used for testing 
# import random

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)
class UserAPI:        
    class _Create(Resource):
        def post(dog):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            id = body.get('id')
            if id is None or len(id) < 0:
                return {'message': f'id has to be at least 1'}, 210
            image = body.get('image')
            if image is None or len(image) < 2:
                return {'message': f'image is missing, or is less than 2 characters'}, 210
            link = body.get('link')
            if link is None or len(link) < 2:
                return {'message': f'link is missing, or is less than 2 characters'}, 210
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'name is missing, or is less than 2 characters'}, 210
            uid = body.get('uid')
            if uid is None or len(uid) < 6:
                return {'message': f'uidis missing, or is less than 2 characters'}, 210
            breed = body.get('breed')
            if breed is None or len(breed) < 2:
                return {'message': f'breed is missing, or is less than 2 characters'}, 210
            sex = body.get('sex')
            if sex is None or len(sex) < 0:
                return {'message': f'sex has to be male or female'}, 210
            price = body.get('price')
            if price is None or len(price) < 2:
                return {'message': f'price has to be at least 100'}, 210
            dob = body.get('dob')
            # validate uid
            # look for password and dob

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(id = id,
                      image=image,
                      link=link,
                      name=name, 
                      uid=uid, 
                      breed=breed, 
                      sex=sex,
                      price=price,
                      )
            
            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            ''' Additional garbage error checking '''
            # set password if provided
            # if password is not None:
            #     uo.set_password(password)
            # # convert to date type
            # if dob is not None:
            #     try:
            #         uo.dob = datetime.strptime(dob, '%m-%d-%Y').date()
            #     except:
            #         return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 210
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'uid {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(dog):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _ReadID(Resource):
        def get(dog, id):
            user = User.query.filter_by(id=id).first()
            if user:
                return jsonify(user.read())
            else:
                return {"message": f"No user found with id {id}"}, 404
    
    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_ReadID, '/<int:id>')
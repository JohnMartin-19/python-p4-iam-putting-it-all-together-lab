#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe


@app.before_request
def check_if_logged_in():
    open_access_list = [
        'signup',
        'signup',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):
        return {'error': '401 Unauthorized'},401
class Signup(Resource):
    def post(self):
        data = request.json
        # Check required fields
        username= data.get('username')
        password=data.get('password')
        image_url = data.get('image_url')
        bio = data.get('bio')

        user = User(
            username=username,
            image_url = image_url,
            bio = bio,
        )

        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(),201
        except IntegrityError:
            return {'error': '422 Unprotected Entity'},422

class CheckSession(Resource):
    def get(self):

        user_id = session['user_id']
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return user.to_dict(),200
        
        return {},401

class Login(Resource):
    def get(self):

        request.json = request.get_json()
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.query.filter(User.username == username).first()

        if user :
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(),200
            return {'error':'401,Unauthorized'},401
        
        
            

class Logout(Resource):
    pass

class RecipeIndex(Resource):
    pass

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
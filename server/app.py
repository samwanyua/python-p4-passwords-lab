#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
         # Setting user's password hash
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session and session['user_id'] is not None:
            user_id = int(session['user_id'])
            # Here we are getting user from database
            user = db.session.get(User, user_id)
            if user:
                return user.to_dict(), 200
        return {'': ''}, 204
    pass

class Login(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter_by(username=json['username']).first()
         # Check if user exists and password is correct
        if user and user.authenticate(json['password']):
            # Set user ID and page views in session
            session['user_id'] = user.id
            session['page_views'] = 0
            return user.to_dict(), 200
        else:
            return {}, 401
    pass

class Logout(Resource):
    def delete(self):
        # clearing session data
        session['page_views'] = None
        session['user_id']=  None
        return {}, 204
    pass

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
import functools
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, abort
from project.server.models import User

def login_required(method):
    @functools.wraps(method)
    def wrapper(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                abort(400, message='Bearer token malformed.')
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            print(resp)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                if(user.is_active):
                    return method(self, user)
            abort(400, message='Provide a valid auth token.')
        else:
            abort(400, message='No auth token')
    return wrapper

def admin_required(method):
    @functools.wraps(method)
    def wrapper(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                abort(400, message='Bearer token malformed.')
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            print(resp)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                if(user.admin):
                    return method(self, user)
                else:
                    abort(400, message='Admin required.')
            abort(400, message='Provide a valid auth token.')
        else:
            abort(400, message='No auth token')
    return wrapper
#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """returns jsonified user object or aborts on incorrect information"""
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({'error': 'email missing'}), 400

    if password is None or password == '':
        return jsonify({'error': 'password missing'}), 400

    user_list = User.search({'email': email})
    if user_list == []:
        return jsonify({'error': 'no user found for this email'}), 404
    user = user_list[0]

    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response

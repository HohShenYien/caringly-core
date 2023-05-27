from functools import wraps

from flask import g, jsonify, request

from server.auth.models import AuthUser
from server.extensions import db


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ""

        if auth_token:
            user = AuthUser.decode_auth_token(auth_token)
            if user is not None:
                g.user = user
                return f(*args, **kwargs)

        return jsonify({"message": "You are unauthenticated", "status": "fail"}), 401

    return decorated_function

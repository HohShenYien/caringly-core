from flask import Blueprint, jsonify, make_response, request

from models import User as UserModel
from server.auth.AuthUser import AuthUser
from server.extensions import Session

auth_blueprint = Blueprint(
    "auth",
    __name__,
)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    post_data = request.get_json()
    session = Session()
    user = session.query(UserModel).filter_by(email=post_data.get("email")).first()
    if not user:
        try:
            user = AuthUser(
                email=post_data.get("email"),
                password=post_data.get("password"),
                username=post_data.get("username"),
            )

            session.add(user)
            session.commit()

            auth_token = user.encode_auth_token()
            responseObject = {
                "status": "success",
                "message": "Successfully registered.",
                "auth_token": auth_token,
            }

            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return make_response(jsonify(responseObject)), 202

from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields

from classes import User as UserModel
from server.auth.extensions import login_required
from server.auth.models import AuthUser
from server.extensions import db
from server.utils import validate_with_schema

auth_blueprint = Blueprint(
    "auth",
    __name__,
)


@auth_blueprint.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({"status": "success", "data": g.user.to_dict()}), 200


class UpdateUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)
    new_password = fields.String()
    receive_email = fields.Bool(required=True)


@auth_blueprint.route("/me", methods=["PUT"])
@login_required
@validate_with_schema(UpdateUserSchema)
def update_me(data: dict):
    if not g.user.match_password(data.get("password")):
        return jsonify({"status": "fail", "message": "Wrong Password!"}), 400
    g.user.email = data.get("email")
    g.user.username = data.get("username")
    g.user.receive_email = data.get("receive_email")
    if "new_password" in data:
        g.user.password = data.get("new_password")
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Updated Successfully!",
                "data": g.user.to_dict(),
            }
        ),
        200,
    )


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


@auth_blueprint.route("/login", methods=["POST"])
@validate_with_schema(LoginSchema)
def login(data):
    post_data = data
    try:
        # fetch the user data
        user = (
            db.session.query(AuthUser).filter_by(email=post_data.get("email")).first()
        )
        if user is None or not user.match_password(data.get("password")):
            return jsonify({"status": "fail", "message": "Incorrect email or password"})
        auth_token = user.encode_auth_token()
        if auth_token:
            responseObject = {
                "status": "success",
                "message": "Successfully logged in.",
                "auth_token": auth_token,
            }
            return jsonify(responseObject), 200
    except Exception as e:
        print(e)
        responseObject = {
            "status": "fail",
            "message": "Something went wrong, please try again",
        }
        return jsonify(responseObject), 500


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)


@auth_blueprint.route("/register", methods=["POST"])
@validate_with_schema(RegisterSchema)
def register(data):
    post_data = data
    user = db.session.query(UserModel).filter_by(email=post_data.get("email")).first()
    if not user:
        try:
            user = AuthUser(
                email=post_data.get("email"),
                password=post_data.get("password"),
                username=post_data.get("username"),
            )

            db.session.add(user)
            db.session.commit()

            auth_token = user.encode_auth_token()
            responseObject = {
                "status": "success",
                "message": "Successfully registered.",
                "auth_token": auth_token,
            }

            return jsonify(responseObject), 201
        except Exception as e:
            responseObject = {
                "status": "fail",
                "message": "Some error occurred. Please try again.",
            }
            return jsonify(responseObject), 400
    else:
        responseObject = {
            "status": "fail",
            "message": "User already exists. Please Log in.",
        }
        return jsonify(responseObject), 202


# TODO: Update User

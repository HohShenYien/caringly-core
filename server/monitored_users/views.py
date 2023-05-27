from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from server.auth.extensions import login_required
from server.extensions import db
from server.monitored_users.extensions import access_monitored_user
from server.monitored_users.models import MonitoredUser
from server.social_accounts.models import SocialAccount
from server.utils import validate_with_schema

monitored_user_blueprint = Blueprint(
    "monitored-users",
    __name__,
)


@monitored_user_blueprint.route("/", methods=["GET"])
@login_required
def all_users():
    users = g.user.monitored_users
    return (
        jsonify(
            {
                "status": "success",
                "data": list(map(lambda x: {"id": x.id, "name": x.name}, users)),
            }
        ),
        200,
    )


class Account(Schema):
    type = fields.String(
        required=True, validate=OneOf(["facebook", "instagram", "twitter"])
    )
    url = fields.URL()


class CreateMonitoredUserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    accounts = fields.Nested(Account(many=True), required=True)


# TODO: Validate the social media URL
@monitored_user_blueprint.route("/", methods=["POST"])
@login_required
@validate_with_schema(CreateMonitoredUserSchema)
def create_monitored_user(data):
    accounts = list(
        map(
            lambda acc: SocialAccount(
                type=acc.get("type"),
                url=acc.get("url"),
                username=data.get("name"),
                social_account_id="asdf",
            ),
            data.get("accounts"),
        )
    )
    monitored_user = MonitoredUser(
        name=data.get("name"),
        email=data.get("email"),
        social_accounts=accounts,
        user_id=g.user.id,
    )
    db.session.add(monitored_user)
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "data": monitored_user.to_dict(),
            }
        ),
        200,
    )


class UpdateMonitoredUserSchema(Schema):
    name = fields.String(required=True)


# TODO: Update User
@monitored_user_blueprint.route("/<monitored_user_id>", methods=["PUT"])
@login_required
@access_monitored_user
@validate_with_schema(UpdateMonitoredUserSchema)
def update_monitored_user(monitored_user_id, monitored_user, data):
    monitored_user.name = data.get("name")
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Updated successfully",
            }
        ),
        200,
    )


@monitored_user_blueprint.route("/<monitored_user_id>", methods=["DELETE"])
@login_required
@access_monitored_user
def delete_monitored_user(monitored_user_id, monitored_user):
    db.session.delete(monitored_user)
    db.session.commit()
    return (
        jsonify({"status": "success", "message": "Deleted successfully"}),
        200,
    )

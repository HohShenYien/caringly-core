# TODO: Validate Social Media URL

from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from server.auth.extensions import login_required
from server.extensions import db
from server.monitored_users.extensions import access_monitored_user
from server.monitored_users.models import MonitoredUser
from server.social_accounts.extensions import access_social_account
from server.social_accounts.models import SocialAccount
from server.utils import validate_with_schema

social_accounts_blueprint = Blueprint(
    "social-accounts",
    __name__,
)


class AccountSchema(Schema):
    type = fields.String(
        required=True, validate=OneOf(["facebook", "instagram", "twitter"])
    )
    url = fields.URL(required=True)


# TODO: Validate the social media URL
@social_accounts_blueprint.route("/", methods=["POST"])
@login_required
@validate_with_schema(AccountSchema)
@access_monitored_user
def create_social_account(data, monitored_user_id, monitored_user: "MonitoredUser"):
    account = SocialAccount(
        type=data.get("type"),
        url=data.get("url"),
        username="ASDF",
        social_account_id="asdf",
    )
    monitored_user.social_accounts.append(account)
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "data": account.to_dict(),
            }
        ),
        200,
    )


@social_accounts_blueprint.route("/<social_account_id>", methods=["PUT"])
@login_required
@validate_with_schema(AccountSchema)
@access_social_account
def update_social_account(
    data, monitored_user_id, social_account_id, social_account: "SocialAccount"
):
    social_account.url = data.get("url")
    social_account.type = data.get("type")
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "data": social_account.to_dict(),
            }
        ),
        200,
    )


@social_accounts_blueprint.route("/<social_account_id>", methods=["DELETE"])
@login_required
@access_social_account
def delete_social_account(
    monitored_user_id, social_account_id, social_account: "SocialAccount"
):
    db.session.delete(social_account)
    db.session.commit()

    return (
        jsonify({"status": "success", "message": "Deleted successfully"}),
        200,
    )

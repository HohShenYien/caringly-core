from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields
from marshmallow.validate import OneOf

from server.auth.extensions import login_required
from server.extensions import db
from server.monitored_users.extensions import access_monitored_user
from server.monitored_users.models import MonitoredUser
from server.social_accounts.extensions import access_social_account
from server.social_accounts.models import SocialAccount
from server.social_media import to_social_media_account
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


# TODO: Change URL to email for facebook
@social_accounts_blueprint.route("/", methods=["POST"])
@login_required
@validate_with_schema(AccountSchema)
@access_monitored_user
def create_social_account(data, monitored_user_id, monitored_user: "MonitoredUser"):
    try:
        account = SocialAccount(
            **to_social_media_account(
                type=data.get("type"),
                url=data.get("url"),
            )
        )
        for acc in monitored_user.social_accounts:
            if acc.url == account.url:
                raise Exception("The account has already existed")
        monitored_user.social_accounts.append(account)

    except Exception as e:
        return (
            jsonify({"status": "fail", "message": str(e)}),
            400,
        )
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
    account = to_social_media_account(
        type=data.get("type"),
        url=data.get("url"),
    )
    social_account.url = account.get("url")
    social_account.type = account.get("type")
    social_account.username = account.get("username")
    social_account.profile_pic_url = account.get("profile_pic_url")
    social_account.social_account_id = account.get("social_account_id")
    social_account.last_scanned = account.get("last_scanned")
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

from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from sqlalchemy.sql import func

from server.auth.extensions import login_required
from server.extensions import db
from server.monitored_users.extensions import access_monitored_user
from server.monitored_users.models import MonitoredUser
from server.posts.models import Post
from server.social_accounts.models import SocialAccount
from server.social_accounts.views import AccountSchema
from server.social_media import to_social_media_account
from server.social_media.instagram import (
    get_instagram_posts,
    get_instagram_user_details,
)
from server.utils import extract_date, validate_with_schema

monitored_user_blueprint = Blueprint(
    "monitored-users",
    __name__,
)


@monitored_user_blueprint.route("/", methods=["GET"])
@login_required
def all_users():
    users = (
        MonitoredUser.query()
        .filter(MonitoredUser.user_id == g.user.id)
        .order_by(MonitoredUser.created_at.desc())
    )
    return (
        jsonify(
            {
                "status": "success",
                "data": list(map(lambda x: {"id": x.id, "name": x.name}, users)),
            }
        ),
        200,
    )


class CreateMonitoredUserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email(required=True)
    accounts = fields.Nested(AccountSchema(many=True), required=True)


# TODO: Validate the social media URL
@monitored_user_blueprint.route("/", methods=["POST"])
@login_required
@validate_with_schema(CreateMonitoredUserSchema)
def create_monitored_user(data):
    accounts = list(
        map(
            lambda acc: SocialAccount(
                **to_social_media_account(type=acc.get("type"), url=acc.get("url")),
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


@monitored_user_blueprint.route("/<monitored_user_id>", methods=["GET"])
@login_required
@access_monitored_user
def monitored_user_details(monitored_user_id, monitored_user):
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


@monitored_user_blueprint.route("/<monitored_user_id>/metrics", methods=["GET"])
@login_required
@extract_date
def metrics(monitored_user_id, date):
    filters = [SocialAccount.monitored_user_id == monitored_user_id]
    if date is not None:
        filters.append(Post.date >= date)
    query = (
        db.session.query(Post.category, func.count().label("c"))
        .join(Post.social_account)
        .filter(*filters)
        .group_by(Post.category)
    )

    print(query)

    res = {"neutral": 0, "suicide": 0, "depression": 0, "total": 0}

    for cat, n in query.all():
        res[cat] = n
        res["total"] += n

    return jsonify({"status": "success", "data": res}), 200


@monitored_user_blueprint.route("/<monitored_user_id>/posts/<cat>", methods=["GET"])
@login_required
@extract_date
def posts(monitored_user_id, date, cat):
    filters = [SocialAccount.monitored_user_id == monitored_user_id]
    if date is not None:
        filters.append(Post.date >= date)
    if cat != "all":
        filters.append(Post.category == cat)
    query = db.session.query(Post).join(Post.social_account).filter(*filters)

    res = [sa.to_dict() for sa in query.all()]

    return jsonify({"status": "success", "data": res}), 200


@monitored_user_blueprint.route("/test/<username>", methods=["GET"])
def test(username):
    user = get_instagram_user_details(f"https://instagram.com/{username}")
    print(user)
    # tweets = get_instagram_posts(user["id"])
    # print(tweets)
    return "HI"

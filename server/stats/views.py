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
from server.utils import extract_date, validate_with_schema

stats_blueprint = Blueprint(
    "stats",
    __name__,
)


@stats_blueprint.route("watchlist", methods=["GET"])
@login_required
def watchlist():
    user = g.user
    query = (
        db.session.query(SocialAccount.type, func.count().label("c"))
        .join(SocialAccount.monitored_user)
        .filter(MonitoredUser.user_id == user.id)
        .group_by(SocialAccount.type)
    )

    res = {"facebook": 0, "twitter": 0, "instagram": 0}

    for type, n in query.all():
        res[type] = n

    return jsonify({"status": "success", "data": res}), 200


@stats_blueprint.route("metrics", methods=["GET"])
@login_required
@extract_date
def metrics(date):
    user = g.user
    filters = [MonitoredUser.user_id == user.id]
    if date is not None:
        filters.append(Post.date >= date)
    postsScanned = (
        db.session.query(Post.category, func.count().label("c"))
        .join(Post.social_account)
        .join(SocialAccount.monitored_user)
        .filter(*filters)
        .group_by(Post.category)
    )

    posts = {"neutral": 0, "suicide": 0, "depression": 0, "total": 0}

    for cat, n in postsScanned.all():
        posts[cat] = n
        posts["total"] += n

    # Count the number of users with posts of category "suicide"
    users_with_suicide_posts = (
        db.session.query(MonitoredUser)
        .join(SocialAccount)
        .join(Post)
        .filter(Post.category == "suicide")
        .filter(MonitoredUser.user_id == user.id)
        .filter(Post.date >= date)
        .distinct()
    )

    # Count the number of users with posts of category "depression"
    users_with_depression_posts = (
        db.session.query(MonitoredUser)
        .join(SocialAccount)
        .join(Post)
        .filter(Post.category == "depression")
        .filter(MonitoredUser.user_id == user.id)
        .filter(Post.date >= date)
        .distinct()
    )

    res = {
        "posts": posts,
        "depression": [u.to_dict_simple() for u in users_with_depression_posts],
        "suicide": [u.to_dict_simple() for u in users_with_suicide_posts],
        "total": db.session.query(MonitoredUser)
        .filter(MonitoredUser.user_id == user.id)
        .count(),
    }

    return jsonify({"status": "success", "data": res}), 200

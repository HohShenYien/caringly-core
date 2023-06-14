from flask import Blueprint, g, jsonify
from marshmallow import Schema, fields
from marshmallow.validate import OneOf
from sqlalchemy.sql import func

from server.auth.extensions import login_required
from server.extensions import db
from server.monitored_users.extensions import access_monitored_user
from server.monitored_users.models import MonitoredUser
from server.posts.models import Post
from server.scan.model import predict
from server.social_accounts.models import SocialAccount
from server.utils import extract_date, validate_with_schema

scan_blueprint = Blueprint(
    "sca",
    __name__,
)


class ScanSchema(Schema):
    text = fields.String(required=True)


@scan_blueprint.route("/", methods=["POST"])
@validate_with_schema(ScanSchema)
@login_required
def scan_single(data):
    prediction, probability = predict([data.get("text")])[0]
    return (
        jsonify(
            {
                "prediction": prediction,
                "probability": probability.item() * 100,
                "status": "success",
            }
        ),
        200,
    )

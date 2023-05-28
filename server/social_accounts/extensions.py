from functools import wraps

from flask import g, jsonify, request

from server.extensions import db
from server.social_accounts.models import SocialAccount


def access_social_account(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        social_id = kwargs["social_account_id"]
        social_account = SocialAccount.query().filter_by(id=social_id).one()

        if social_account is None:
            return (
                jsonify(
                    {
                        "message": f"Social Account {social_id} not found",
                        "status": "fail",
                    }
                ),
                404,
            )

        return f(*args, **kwargs, social_account=social_account)

    return decorated_function

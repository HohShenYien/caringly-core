from functools import wraps

from flask import g, jsonify, request

from server.auth.models import AuthUser
from server.extensions import db
from server.monitored_users.models import MonitoredUserImpl


def access_monitored_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        monitored_id = kwargs["monitored_user_id"]
        monitored_user = (
            db.session.query(MonitoredUserImpl).filter_by(id=monitored_id).one()
        )

        if monitored_user is None:
            return (
                jsonify(
                    {
                        "message": f"Monitored User {monitored_id} not found",
                        "status": "fail",
                    }
                ),
                404,
            )

        return f(*args, **kwargs, monitored_user=monitored_user)

    return decorated_function

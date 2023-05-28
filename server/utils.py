from datetime import datetime, timedelta
from functools import wraps

import flask
from dateutil.relativedelta import relativedelta
from flask import jsonify, request
from marshmallow import Schema, ValidationError


def validate_with_schema(Schema: Schema):
    def decorator(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            try:
                schema = Schema()
                data = flask.request.get_json()
                post_data = schema.load(data)
            except ValidationError as err:
                return jsonify({"status": "fail", "message": err.messages}), 400
            return f(*args, **kwargs, data=post_data)

        return wrapped_f

    return decorator


def extract_date(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = None
        date_string = request.args.get("date")
        current_date = datetime.now()
        match date_string:
            case "year":
                res = current_date - relativedelta(years=1)
            case "month":
                res = current_date - relativedelta(months=1)
            case "week":
                res = current_date - timedelta(weeks=1)

        if res:
            res = res.date()

        return f(*args, **kwargs, date=res)

    return decorated_function

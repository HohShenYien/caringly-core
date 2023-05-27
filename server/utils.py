from functools import wraps

import flask
from flask import jsonify
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

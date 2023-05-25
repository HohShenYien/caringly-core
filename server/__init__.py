from flask import Flask

from server.auth.views import auth_blueprint
from server.extensions import bcrypt, config


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/."""
    app = Flask(__name__.split(".")[0])
    # app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    print(app.url_map)
    return app


def register_secrets(app: "Flask"):
    app.config["SECRET_KEY"] = config["SECRET_KEY"]


def register_blueprints(app: "Flask"):
    app.register_blueprint(auth_blueprint, url_prefix="/auth")


def register_extensions(app: "Flask"):
    bcrypt.init_app(app)

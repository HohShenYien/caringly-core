from flask import Flask

from server.auth.views import auth_blueprint
from server.extensions import bcrypt, config, db
from server.monitored_users.views import monitored_user_blueprint


def create_app():
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/."""
    app = Flask(__name__.split(".")[0])
    # app.config.from_object(config_object)
    register_secrets(app)
    register_extensions(app)
    register_blueprints(app)
    print(app.url_map)
    return app


def register_secrets(app: "Flask"):
    app.config["SECRET_KEY"] = config["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = config["DB_URL"]


def register_blueprints(app: "Flask"):
    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(monitored_user_blueprint, url_prefix="/monitored-users")


def register_extensions(app: "Flask"):
    bcrypt.init_app(app)
    db.init_app(app)

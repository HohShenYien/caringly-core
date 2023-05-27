from dotenv import dotenv_values
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

config = dotenv_values()

bcrypt = Bcrypt()
db = SQLAlchemy()

from dotenv import dotenv_values
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

config = dotenv_values()
engine = create_engine(config["DB_URL"], echo=True, future=True)

bcrypt = Bcrypt()
Session = sessionmaker(engine)

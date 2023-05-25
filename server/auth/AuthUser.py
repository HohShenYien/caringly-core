from datetime import datetime, timedelta

import jwt

from models import User as UserModel
from server.auth.utils import is_valid_uuid
from server.extensions import Session, bcrypt, config


class AuthUser(UserModel):
    def __init__(self, username: str, email: str, password: str):
        super(UserModel, self).__init__(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password),
        )

    def encode_auth_token(self) -> str:
        """
        Generates the Auth Token
        """
        print("MY secret IS", config["SECRET_KEY"])
        payload = {
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "sub": self.id,
        }
        return jwt.encode(payload, config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    @staticmethod
    def decode_auth_token(auth_token: str) -> "AuthUser":
        """
        Decodes the auth token
        """
        try:
            session = Session()
            payload = jwt.decode(auth_token, config["SECRET_KEY"])
            if is_valid_uuid():
                user = session.query(UserModel).filter(id=payload["sub"].one())
                if user is not None:
                    return user
                raise Exception("User not found")
            raise Exception(jwt.InvalidTokenError)
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

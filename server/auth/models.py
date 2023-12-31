from datetime import datetime, timedelta

import jwt

from server.auth.utils import is_valid_uuid
from server.extensions import bcrypt, config, db
from server.users.models import User


class AuthUser(User):
    def __init__(self, username: str, email: str, password: str):
        super(User, self).__init__(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password).decode("utf8"),
        )

    def match_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def encode_auth_token(self) -> str:
        """
        Generates the Auth Token
        """
        payload = {
            "exp": datetime.utcnow() + timedelta(days=7),
            "iat": datetime.utcnow(),
            "sub": self.id,
        }
        return jwt.encode(payload, config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def decode_auth_token(auth_token: str) -> "AuthUser":
        """
        Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, config["SECRET_KEY"], algorithms=["HS256"])
            if is_valid_uuid(payload["sub"]):
                user = db.session.query(AuthUser).filter_by(id=payload["sub"]).one()
                if user is not None:
                    return user
                raise Exception("User not found")
            raise Exception(jwt.InvalidTokenError)
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError as e:
            return "Invalid token. Please log in again."
        except Exception:
            return "Something went wrong, please try to login again"

import jwt

from classes import SocialAccount as SocialAccountModel
from server.extensions import db


class SocialAccountImpl(SocialAccountModel):
    def __init__(self, *args, **kwargs):
        super(SocialAccountImpl, self).__init__(*args, **kwargs)

    def to_dict(self):
        return {
            "type": self.type,
            "username": self.username,
            "url": self.url,
            "id": self.id,
        }

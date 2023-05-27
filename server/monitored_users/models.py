from datetime import datetime, timedelta

import jwt

from classes import MonitoredUser as MonitoredUserModel
from server.extensions import db
from server.social_accounts.models import SocialAccountImpl


class MonitoredUserImpl(MonitoredUserModel):
    def __init__(self, *args, **kwargs):
        super(MonitoredUserImpl, self).__init__(*args, **kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "accounts": list(
                map(lambda acc: SocialAccountImpl.to_dict(acc), self.social_accounts)
            ),
        }

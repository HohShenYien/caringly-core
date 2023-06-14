import re
from datetime import datetime
from urllib.parse import quote

import requests

from server.extensions import config


def get_twitter_user_details(url: str):
    username = re.match(r"https://(www\.)?twitter\.com/([a-zA-Z0-9_]+)/?", url).group(2)
    try:
        response = requests.get(
            quote(f"{config['FRONTEND_URL']}/api/twitter/users/{username}")
        )
        if response.status_code != 200:
            raise Exception("")
    except Exception as e:
        print(e)
        raise Exception("The Twitter user does not exist")

    return response.json()["user"]


def get_tweets(id: str, last_scanned: "datetime"):
    try:
        response = requests.get(
            f"{config['FRONTEND_URL']}/api/twitter/tweets/{id}?last_scanned={last_scanned.isoformat()}"
        )
        if response.status_code != 200:
            raise Exception("")
    except Exception as e:
        print(e)
        raise Exception("Please try again later")

    return list(
        map(
            lambda x: {"text": x.get("fullText"), "date": x.get("createdAt")},
            response.json().get("tweets"),
        )
    )

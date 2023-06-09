import re

import requests

from server.extensions import config


def get_twitter_user_details(url: str):
    username = re.match(r"https://twitter.com/([a-zA-Z0-9_]+)", url).group(1)
    try:
        response = requests.get(
            f"{config['FRONTEND_URL']}/api/twitter/users/{username}"
        )
    except Exception as e:
        print(e)
        raise Exception("Invalid user")

    return response.json()["user"]


def get_tweets(id):
    try:
        response = requests.get(f"{config['FRONTEND_URL']}/api/twitter/tweets/{id}")
    except:
        raise Exception("Try again")

    return response.json()

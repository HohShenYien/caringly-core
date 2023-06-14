import re
from datetime import datetime
from os import path

from instagrapi import Client
from instagrapi.exceptions import LoginRequired
from instagrapi.types import Relationship, User, UserShort

from server.extensions import config

session_path = "./session.json"


cl = Client(request_timeout=7)
if not path.exists(session_path):
    print("Not exists")
    with open(session_path, "w") as f:
        f.write("{}")
else:
    cl.load_settings(session_path)
# TODO: uncomment
# cl.login(config["INSTA_USERNAME"], config["INSTA_PASSWORD"])
# cl.delay_range = [3, 5]
# cl.dump_settings(session_path)


def get_instagram_user_details(url: str) -> User:
    username = re.match(
        r"https:\/\/(www\.)?instagram\.com\/([a-zA-Z0-9_]+)", url
    ).group(2)
    try:
        user_id = cl.user_id_from_username(username)
        info = cl.user_info(user_id)
        print(info)

    except Exception as e:
        print(e)
        raise Exception("The Instagram user does not exist")

    return info


def get_instagram_posts(id: str, date_after: "datetime"):
    try:
        response = cl.user_medias_paginated(id, 10)
    except:
        raise Exception("Try again")

    return response
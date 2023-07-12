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

cl.login(config["INSTA_USERNAME"], config["INSTA_PASSWORD"])
cl.delay_range = [3, 5]
cl.dump_settings(session_path)


def get_instagram_user_details(url: str) -> User:
    username = re.match(
        r"https:\/\/(www\.)?instagram\.com\/([a-zA-Z0-9_]+)", url
    ).group(2)
    try:
        user_id = cl.user_id_from_username(username)
        info = cl.user_info(user_id)

    except Exception as e:
        print(e)
        raise Exception("The Instagram user does not exist")

    return info


def get_instagram_posts(id: str, date_after: "datetime"):
    res = []
    try:
        response, cursor = cl.user_medias_paginated(id, 10)
        flag = True

        while flag:
            if len(res) > 0:
                response, cursor = cl.user_medias_paginated(id, 10, cursor)
            for media in response:
                if media.taken_at.replace(tzinfo=None) < date_after:
                    flag = False
                    break
                res.append(
                    {
                        "id": media.id,
                        "url": f"https://instagram.com/p/{media.code}/",
                        "text": media.caption_text,
                        "date": media.taken_at.replace(tzinfo=None),
                    }
                )

            if len(response) < 10:
                flag = False
    except Exception as e:
        print(e)
        raise Exception("Try again")

    return res

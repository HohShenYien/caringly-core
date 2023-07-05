from datetime import datetime
from typing import List

from server.extensions import db
from server.posts.models import Post
from server.scan.model import predict
from server.social_accounts.models import SocialAccount
from server.social_media.instagram import get_instagram_posts
from server.social_media.twitter import get_tweets


def scan_account_posts(social_account: "SocialAccount") -> "List[SocialAccount]":
    posts = []
    try:
        match social_account.type:
            case "twitter":
                posts = get_tweets(
                    social_account.url.split("/").pop(), social_account.last_scanned
                )
            case "instagram":
                posts = get_instagram_posts(
                    social_account.social_account_id, social_account.last_scanned
                )

        texts = [post.get("text") for post in posts]
        predictions = predict(texts)

        mapped_posts = []
        for i in range(len(posts)):
            prediction, probability = predictions[i]
            mapped_posts.append(
                Post(
                    category=prediction,
                    probability=probability,
                    url=posts[i].get("url"),
                    date=posts[i].get("date"),
                    text=posts[i].get("text"),
                )
            )

        social_account.posts.extend(mapped_posts)
        social_account.last_scanned = datetime.now()
        db.session.commit()

        return mapped_posts
    except Exception as e:
        print(e)
        return []

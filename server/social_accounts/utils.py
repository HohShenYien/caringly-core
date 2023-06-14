from datetime import datetime
from typing import List

from server.extensions import db
from server.posts.models import Post
from server.social_accounts.models import SocialAccount
from server.social_media.instagram import get_instagram_posts
from server.social_media.twitter import get_tweets


def scan_account_posts(social_account: "SocialAccount") -> "List[SocialAccount]":
    posts = []
    match social_account.type:
        case "twitter":
            posts = get_tweets(
                social_account.social_account_id, social_account.last_scanned
            )
        case "instagram":
            posts = get_instagram_posts(
                social_account.social_account_id, social_account.last_scanned
            )

    mapped_posts = list(
        map(lambda x: Post(category="neutral", probability=0.99, **x), posts)
    )
    social_account.posts.extend(mapped_posts)
    social_account.last_scanned = datetime.now()
    db.session.commit()

    return mapped_posts

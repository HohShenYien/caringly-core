from datetime import datetime

from server.social_media.instagram import get_instagram_user_details
from server.social_media.twitter import get_twitter_user_details

TWITTER_START_DATE = "21/03/2006"
INSTAGRAM_START_DATE = "06/10/2010"


def to_social_media_account(url: str, type: str):
    match type:
        case "twitter":
            user = get_twitter_user_details(url)
            return {
                "username": user["fullName"],
                "url": f"https://twitter.com/{user['userName']}",
                "social_account_id": user["id"],
                "profile_pic_url": user["profileImage"],
                "type": type,
                "last_scanned": datetime.strptime(TWITTER_START_DATE, "%d/%m/%Y"),
            }
        case "instagram":
            user = get_instagram_user_details(url)
            return {
                "username": user.username,
                "url": f"https://www.instagram.com/{user.username}",
                "social_account_id": user.pk,
                "profile_pic_url": user.profile_pic_url,
                "type": type,
                "last_scanned": datetime.strptime(INSTAGRAM_START_DATE, "%d/%m/%Y"),
            }

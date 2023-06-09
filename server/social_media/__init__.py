from server.social_media.twitter import get_twitter_user_details


def to_social_media_account(url: str, type: str):
    match type:
        case "twitter":
            user = get_twitter_user_details(url)
            return {
                "username": user["fullName"],
                "url": url,
                "social_account_id": user["id"],
                "profile_pic_url": user["profileImage"],
                "type": type,   
            }
            
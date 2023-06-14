from server.monitored_users.models import MonitoredUser
from server.social_accounts.utils import scan_account_posts


def scan_user_posts(user: MonitoredUser):
    posts = list(map(lambda x: scan_account_posts(x), user.social_accounts))

    # Flatten
    return [p for sublist in posts for p in map(lambda post: post.to_dict(), sublist)]

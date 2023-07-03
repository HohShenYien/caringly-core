import time
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from server.email import send_alert
from server.extensions import config
from server.monitored_users.models import MonitoredUser
from server.monitored_users.utils import scan_user_posts

scheduler = BackgroundScheduler()


def scan_account():
    all_monitored_users = MonitoredUser.query().all()  # type: List[MonitoredUser]
    for monitored_user in all_monitored_users:
        posts = scan_user_posts(monitored_user)
        dangerous_posts = []
        for post in posts:
            if post.get("category") != "neutral":
                dangerous_posts.append(post)
        if len(dangerous_posts) > 0:
            send_alert(monitored_user.user, monitored_user, dangerous_posts)

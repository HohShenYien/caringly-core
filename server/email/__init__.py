import atexit
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import join
from typing import List

from server.extensions import config
from server.monitored_users.models import MonitoredUser
from server.users.models import User

TEMPLATE_PATH = "./server/email/templates"

mailer = smtplib.SMTP(config.get("MAIL_SERVER"), int(config.get("MAIL_PORT")))
mailer.login(config.get("MAIL_USERNAME"), config.get("MAIL_PASSWORD"))
atexit.register(lambda: mailer.quit())
sender = config.get("MAIL_SENDER")


def send_email(subject, html, recipient):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    content = MIMEText(html, "html")

    msg.attach(content)

    mailer.sendmail(sender, recipient, msg.as_string())

    return True


def read_template(name: str, variables: dict = {}):
    html = open(join(TEMPLATE_PATH, f"{name}.html")).read()
    html = html.replace(f"{{FRONTEND_URL}}", config.get("FRONTEND_URL"))
    for key, value in variables.items():
        html = html.replace(f"{{{key}}}", value)
    return html


def send_alert(user: User, monitored_user: MonitoredUser, posts: "List[dict]"):
    url = f"{config.get('FRONTEND_URL')}/app/users/{monitored_user.id}"
    print(posts)
    content = map(
        lambda post: f"""\
                  <tr>
                    <td
                        style="
                        padding-bottom: 10px;
                        padding-left: 10px;
                        padding-right: 10px;
                        "
                    >
                        <div style="font-family: sans-serif">
                            <div
                                class="{"red" if post.get(" category") == "suicide" else "orange"} post"
                                style="
                                font-size: 14px;
                                font-family: Tahoma, Verdana,
                                    Segoe, sans-serif;
                                mso-line-height-alt: 14.399999999999999px;
                                color: #8d94a3;
                                line-height: 1.2;
                                "
                            >
                                <div style="display: flex;align-items: flex-start;">
                                    <img src="{"https://i.imgur.com/nFHPZ84.png" if post.get("type") == "instagram" else "https://i.imgur.com/AphCJD1.png"}" alt="Social media logo" style="height: 36px;width: 36px;object-fit: contain;">
                                    <div style="padding-left: 10px;padding-right: 10px;">
                                        <p style="color: black;text-transform: capitalize;font-weight: 600;margin: 0;">{post.get("type")}</p>
                                        <p style="margin: 0; margin-top: 3px;">{post.get("date").strftime("%m/%d/%Y")}</p>
                                    </div>
                                    <div style="flex: 1;display: flex;">
                                        <div style="font-size: 10px;font-weight: 600;padding: 2px 4px;border-radius: 50px;text-transform: capitalize;" class="{"red-pill" if post.get("category") == "suicide" else "orange-pill"}">{post.get("category")}</div>
                                    </div>
                                    <a href="{post.get("url")}" target="_blank">
                                        <span>Open the post</span> 
                                        <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                                    </a>
                                </div>
                                <p style="
                                    margin: 0;
                                    margin-top: 8px;
                                    font-size: 16px;
                                    color: black;
                                ">
                                    {post.get("text")}
                                </p>
                            </div>
                        </div>
                    </td>
                    </tr>
                  """,
        posts,
    )
    html = read_template(
        "alert",
        {
            "url": url,
            "name": user.username,
            "monitored_user": monitored_user.name,
            "content": "".join(content),
        },
    )
    send_email("Caringly: Dangerous post detected", html, user.email)

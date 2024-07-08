from lib.xapi import *
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

notifs = sesh.get_notifications()
for type, date, seen, blob in zip(map(NotificationType, notifs["type"]), notifs["date"], notifs["seen"], notifs["blob"]):
    print(blob["username"] + ", " + date)

    if type in (NotificationType.POST, NotificationType.REPLY):
        print(blob["text"] + " " + blob["shadername"] + ":")
        print(blob["comment"])

    elif type == NotificationType.FOLLOW:
        print(blob["text"])

    elif type == NotificationType.PUBLISH:
        print(blob["text"] + " " + blob["shadername"])

    elif type == NotificationType.LIKE:
        print(blob["text"] + " " + blob["shadername"])

    if seen == 1:
        print("[seen]")

    print("-" * 40)

sesh.signout()
sesh.close()

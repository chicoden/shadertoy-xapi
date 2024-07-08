from lib.xapi import *
from datetime import datetime
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

shader_id = input("Test shader ID (or type \"auto\"): ")
if shader_id == "auto":
    shaders = sesh.get_shaders(sesh.get_all_shaders(only_public=True))
    most_likes = -1
    popular_shader = None
    for shader in shaders:
        if shader["info"]["likes"] > most_likes:
            most_likes = shader["info"]["likes"]
            popular_shader = shader

    shader = popular_shader

else:
    shader, = sesh.get_shaders([shader_id])

comments = sesh.get_comments(shader["info"]["id"])
for username, date, text, hidden, id in zip(comments["username"], comments["date"], comments["text"], comments["hidden"], comments["id"]):
    print("Comment ID:", id)
    print(username, "posted on", datetime.utcfromtimestamp(int(date)).strftime("%Y-%m-%d"))
    print(text, end = "[hidden]\n" if hidden == 1 else "\n")
    print("-" * 40)

sesh.signout()
sesh.close()

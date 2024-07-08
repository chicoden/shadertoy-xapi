from lib.xapi import *
from datetime import datetime
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

shader, = sesh.get_shaders(["Dd3GR8"])
print(shader["info"]["name"])
date = datetime.utcfromtimestamp(int(shader["info"]["date"])).strftime("%Y-%m-%d")
print("Created by", shader["info"]["username"], "on", date)
print("Likes before:", shader["info"]["likes"])

sesh.set_shader_like("Dd3GR8", True)
print("Liked shader")

shader, = sesh.get_shaders(["Dd3GR8"])
print("Likes after:", shader["info"]["likes"])

sesh.set_shader_like("Dd3GR8", False)
print("Unliked shader")

if sesh.report_shader("Dd3GR8"):
    print("Reported shader")

if sesh.report_crash("Dd3GR8"):
    print("Reported crash")

sesh.signout()
sesh.close()

from lib.xapi import *
from datetime import datetime
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

shader_id = input("Test shader ID: ")
comment_id = input("Test comment ID: ")
comments = sesh.get_comments(shader_id)
hidden = 1 - comments["hidden"][comments["id"].index(comment_id)]
if sesh.set_comment_visibility(shader_id, comment_id, not hidden):
    print("Comment is now", "hidden" if hidden else "visible")

sesh.signout()
sesh.close()

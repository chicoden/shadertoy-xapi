from lib.xapi import *
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

try:
    comments = sesh.post_comment(input("Test shader ID: "), input("Comment to post: "))
    print("Comment posted with ID", comments["id"][0])

finally:
    sesh.signout()
    sesh.close()

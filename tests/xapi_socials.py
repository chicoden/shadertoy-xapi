from lib.xapi import *
from itertools import zip_longest
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

socials = sesh.get_socials()
following = socials["following"]["username"]
followers = socials["followers"]["username"]

username = None
if "oneshade" not in following:
    if input("Follow oneshade? (y/n) ") == "y":
        if sesh.set_following("oneshade", True):
            print("Yay! You are now following oneshade.")

    else:
        print("...")
        username = input("Who do want to follow then? ")

if username is None:
    username = input("Enter a user to follow: ")

if username and username not in following:
    if sesh.set_following(username, True):
        print("Followed", username)

socials = sesh.get_socials()
following = socials["following"]["username"]
followers = socials["followers"]["username"]

padlen = max(map(len, following + ["Following:"]))
print("Following:".ljust(padlen), "Followers:".ljust(padlen), sep="    ")
for followee, follower in zip_longest(following, followers, fillvalue=""):
    print(followee.ljust(padlen), follower.ljust(padlen), sep="    ")

sesh.signout()
sesh.close()

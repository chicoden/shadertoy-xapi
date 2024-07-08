from lib.xapi import *
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

sesh.create_app(input("App name: "), input("App description: "))
print("Now go to https://www.shadertoy.com/myapps and find the app key")
if sesh.delete_app(input("App key: ")):
    print("App deleted")

sesh.signout()
sesh.close()

from lib.xapi import *
import os

sesh = ShadertoySession()

try:
    sesh.signin(
        os.getenv("SHADERTOY_USERNAME") or input("Username: "),
        os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
    )

    print("Sign in success!")

except ShadertoyError:
    print("Sign in failed :(")

finally:
    sesh.signout()
    print("Signed out")
    sesh.close()

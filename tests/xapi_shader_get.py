from lib.xapi import *
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

shaders = sesh.get_shaders(sesh.get_all_shaders()[:5])
for shader in shaders:
    print("Shader \"" + shader["info"]["name"] + "\" has", shader["info"]["likes"], "likes")

sesh.signout()
sesh.close()

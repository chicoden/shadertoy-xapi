from lib.xapi import *
import random
import uuid
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

shader, = sesh.get_shaders([random.choice(sesh.get_all_shaders())])
fork_id = sesh.upload_shader(shader, is_fork=True)
print("\"" + shader["info"]["name"] + "\" fork at https://www.shadertoy.com/view/" + fork_id)

fork, = sesh.get_shaders([fork_id])
print(fork["info"]["name"])
fork["info"]["name"] = "random name " + uuid.uuid4().hex[:6]
print(sesh.upload_shader(fork, is_update=True))
fork_new, = sesh.get_shaders([fork_id])
print(fork["info"]["name"])

if sesh.delete_shader(fork_id):
    print("Deleted", fork_id)

if len(sesh.get_shaders([fork_id])) == 0:
    print("Fork no longer exists")

sesh.signout()
sesh.close()

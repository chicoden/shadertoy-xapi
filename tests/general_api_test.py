from lib.api import *
import os

app_key = os.getenv("SHADERTOY_APP_KEY") or input("App key: ")
app = ShadertoyApp(app_key)

fluid_sims = app.query(["fluid", "simulation"], sort_by="love", filter="multipass", num_shaders=5)
print(fluid_sims)

for shader_id in fluid_sims:
    shader = app.get_shader(shader_id)
    print("Shader \"" + shader["info"]["name"] + "\" has", shader["info"]["likes"], "likes")

all_shader_ids = app.get_all_shaders()
print(len(all_shader_ids), "public+api shaders on shadertoy currently")

import io
from PIL import Image
shader = app.get_shader("tsdBW4")
media_path = shader["renderpass"][0]["inputs"][0]["src"]
#ext = media_path.rsplit(".", maxsplit=1)[-1]
file = io.BytesIO(app.get_raw_media(media_path))
Image.open(file).show()
file.close()

app.close()

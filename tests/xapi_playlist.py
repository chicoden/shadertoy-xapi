from lib.xapi import *
import uuid
import os

sesh = ShadertoySession()
sesh.signin(
    os.getenv("SHADERTOY_USERNAME") or input("Username: "),
    os.getenv("SHADERTOY_PASSWORD") or input("Password: ")
)

playlist_id = sesh.create_playlist("fuzzy wuzzy " + uuid.uuid4().hex[:6], "fuzzwuzz", PlaylistPrivacy.UNLISTED)
print("Playlist", playlist_id, "created")

playlists = sesh.get_playlists()
print("It is titled \"" + playlists["name"][playlists["id"].index(playlist_id)] + "\"")

sesh.set_playlist_metadata(playlist_id, "fuzzy wuzzy still " + uuid.uuid4().hex[:6], "still fuzzwuzz", PlaylistPrivacy.UNLISTED)
playlists = sesh.get_playlists()
print(len(playlists["id"]), "playlists currently")
print("Name changed to \"" + playlists["name"][playlists["id"].index(playlist_id)] + "\"")

shader, = sesh.get_shaders(sesh.get_all_shaders()[:1])
shader_id = shader["info"]["id"]

sesh.add_shader_to_playlist(shader_id, playlist_id)
stats = sesh.get_shader_playlist_stats(shader_id)
if stats["exists"][stats["id"].index(playlist_id)] == 1:
    print("Shader \"" + shader["info"]["name"] + "\" now in playlist")

sesh.remove_shader_from_playlist(shader_id, playlist_id)
stats = sesh.get_shader_playlist_stats(shader_id)
if stats["exists"][stats["id"].index(playlist_id)] == 0:
    print("Shader \"" + shader["info"]["name"] + "\" removed from playlist")

sesh.delete_playlist(playlist_id)
print(len(sesh.get_playlists()["id"]), "playlists now")

sesh.signout()
sesh.close()

"""
An implementation of a client for the Shadertoy Public API.
Implements the features documented in https://www.shadertoy.com/howto
To access the API, you need an API key which can be created
at https://www.shadertoy.com/myapps (once you are signed in)

>>> from lib.api import ShadertoyApp
>>> app = ShadertoyApp("my_app_key")
>>> app.query(["fluid", "simulation"], sort_by="newest", num_shaders=5)
['MfG3Rt', 'lXB3WG', 'lXB3z3', 'lXSGz3', 'M3sGDf']

>>> app = ShadertoyApp()
>>> app.get_raw_media("/media/previz/buffer00.png")
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00...'
"""

import requests

SHADERTOY_BASE_URL = "https://www.shadertoy.com"
SHADERTOY_API_BASE_URL = "https://www.shadertoy.com/api/v1"
SHADERTOY_CLASSIFIERS = ("name", "love", "popular", "newest", "hot")
SHADERTOY_FILTERS = ("vr", "soundoutput", "soundinput", "webcam", "multipass", "musicstream")

class ShadertoyAPIError(Exception):
    pass

def _check_error(json):
    if "Error" in json:
        raise ShadertoyAPIError(json["Error"])

class ShadertoyApp:
    def __init__(self, app_key=None):
        self.key = app_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "shadertoy-client"
        })

    def require_key(self):
        """ Raises a ShadertoyAPIError if the app key is not initialized. """
        if self.key is None:
            raise ShadertoyAPIError("app key required")

    def query(self, keywords, sort_by=None, filter=None, start_index=0, num_shaders=-1):
        """
        Queries the shadertoy API for shaders matching the given keywords,
        sorted by the classifier sort_by, filtered by the given filter,
        starting from the given index and limited to num_shaders.
        Note: num_shaders is -1 by default, meaning there will be no limit
        on how many shaders will be returned.
        """

        self.require_key()
        url = SHADERTOY_API_BASE_URL + "/shaders/query/" + "+".join(keywords) + "?key=" + self.key
        if sort_by is not None:
            url += "&sort=" + sort_by

        if filter is not None:
            url += "&filter=" + filter

        if start_index > 0:
            url += "&from=" + str(start_index)

        if num_shaders > -1:
            url += "&num=" + str(num_shaders)

        json = self.session.get(url).json()
        _check_error(json)
        return json.get("Results", [])

    def get_shader(self, shader_id):
        """
        Retrieves shader shader_id encoded in JSON format.
        I recommend testing this method out and taking a look at the JSON
        yourself to get familiar with the structure.
        """

        self.require_key()
        url = SHADERTOY_API_BASE_URL + "/shaders/" + shader_id + "?key=" + self.key
        json = self.session.get(url).json()
        _check_error(json)
        return json["Shader"]

    def get_all_shaders(self):
        """ Retrieves a list of all public+api shader IDs. """
        self.require_key()
        url = SHADERTOY_API_BASE_URL + "/shaders?key=" + self.key
        json = self.session.get(url).json()
        _check_error(json)
        return json.get("Results", [])

    def get_raw_media(self, path):
        """
        Retrieves the raw media file from the given path
        (relative to shadertoy.com)
        """

        url = SHADERTOY_BASE_URL + path
        response = self.session.get(url)
        if response.status_code // 100 in (4, 5):
            raise ShadertoyAPIError(response.reason)

        return response.content

    def close(self):
        """ Closes the app session. Call this when you are done using it. """
        self.session.close()

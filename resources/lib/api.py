from __future__ import unicode_literals
from resources.lib.utils import update_query_params, deep_get
import urlquick
from resources.lib.constants import URLS, BASE_HEADERS, url_constructor
from codequick import Script
import requests


class MiniTvApi:
    def __init__(self):
        self.session = urlquick.Session()
        self.session.headers.update(BASE_HEADERS)

    def get_page(self, category, cursor):
        url = url_constructor(URLS.get("PAGE"))
        url = update_query_params(url, {"category": category, "cursor": cursor})
        resp = self.get(url)
        return resp.get("widgets"), resp.get("paginationProps")

    def get_content(self, id):
        url = url_constructor(URLS.get("CONTENT"))
        url = update_query_params(url, {"contentId": id})
        resp = self.get(url)
        return resp

    def get_seasons(self, id, cursor):
        url = url_constructor(URLS.get("CONTENT"))
        url = update_query_params(url, {"contentId": id, "cursor": cursor})
        resp = self.get(url)
        return deep_get(resp.get("widgets")[0], "data.options")

    def get_episodes(self, id):
        url = url_constructor(URLS.get("EPISODE"))
        url = f"""{url}/{id}"""
        resp = self.get(url)
        return deep_get(resp, "data.widgets")[0]

    def get_video(self, id):
        url = url_constructor(URLS.get("CONTENT"))
        url = update_query_params(url, {"contentId": id})
        resp = self.get(url)
        return resp.get("widgets")[0]

    def raw_post(self, url, headers, payload):
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 401:
                Script.notify("Error", "")
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "post")

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, **kwargs)
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "get", **kwargs)

    def post(self, url, **kwargs):
        try:
            response = self.session.post(url, **kwargs)
            return response.json()
        except Exception as e:
            return self._handle_error(e, url, "post", **kwargs)

    def _handle_error(self, e, url, _rtype, **kwargs):
        Script.notify("Internal Error", "")

    def _get_play_headers(self):
        stream_headers = self.session.headers
        return stream_headers

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.utils import deep_get
from resources.lib.api import MiniTvApi
from resources.lib.builder import Builder
import urlquick
from codequick import Route, run, Script, Resolver
from codequick.script import Settings
from uuid import uuid4


@Route.register
def root(_):
    yield from builder.build_menu()


@Route.register
def list_collection(_, **kwargs):
    if "category" in kwargs:
        while kwargs.get("hasNextPage"):
            page, pagination = api.get_page(
                kwargs.get("category"), kwargs.get("nextCursor")
            )
            kwargs["hasNextPage"] = pagination.get("hasNextPage")
            kwargs["nextCursor"] = pagination.get("nextCursor")

            yield from builder.build_collection(page)
    else:
        return False


@Route.register
def list_page(_, **kwargs):
    if "items" in kwargs:
        yield from builder.build_page(kwargs.get("items"))
    else:
        return False


@Route.register(redirect_single_item=True)
def list_content(_, **kwargs):
    if "id" in kwargs:
        content = api.get_content(kwargs.get("id"))
        vodType = deep_get(content, "metaData.contentDetails.vodType")
        if vodType == "MOVIE":
            yield from builder.build_item(deep_get(content, "widgets"))
        else:
            cursor = deep_get(content, "paginationProps.nextCursor")
            seasons = api.get_seasons(kwargs.get("id"), cursor)
            yield from builder.build_seasons(seasons)
    else:
        yield False


@Route.register
def list_episodes(_, **kwargs):
    if "id" in kwargs:
        episodes = api.get_episodes(kwargs.get("id"))
        yield from builder.build_item(deep_get(episodes, "data.widgets"))
    else:
        yield False


@Resolver.register
def play_video(_, **kwargs):
    if "id" in kwargs:
        video = api.get_video(kwargs.get("id"))
        stream_headers = api._get_play_headers()
        return builder.build_play(video, stream_headers)


@Script.register
def cleanup(_):
    urlquick.cache_cleanup(-1)
    Script.notify("Cache Cleaned", "")


@Script.register
def generate_deviceid(_):
    device_id = uuid4().hex
    Settings().__setitem__("device_id", device_id)


api = MiniTvApi()
builder = Builder()

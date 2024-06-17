# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.utils import get_images, deep_get
from resources.lib.constants import MAIN_MENU
from codequick import Listitem, Resolver, Route
import inputstreamhelper
from urllib.parse import urlencode


class Builder:
    def build_menu(self):
        for item_name, category, image in MAIN_MENU:
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_collection"),
                "label": item_name,
                "params": {"category": category, "hasNextPage": True, "nextCursor": ""},
            }
            item = Listitem.from_dict(**item_data)
            item.art.local_thumb(image)
            yield item

    def build_collection(self, items):
        for each in items:
            if each.get("type") == "LIST":
                thumb, fanart = get_images(deep_get(each, "data.widgets")[0])
                item_data = {
                    "callback": Route.ref("/resources/lib/main:list_page"),
                    "label": deep_get(each, "data.title"),
                    "art": {"thumb": thumb, "fanart": fanart},
                    "params": {"items": deep_get(each, "data.widgets")},
                }
                yield Listitem.from_dict(**item_data)

    def build_page(self, items):
        for each in items:
            thumb, fanart = get_images(each)
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_content"),
                "label": deep_get(each, "data.analytics.contentCard.name"),
                "art": {"thumb": thumb, "fanart": fanart},
                "params": {"id": deep_get(each, "data.analytics.contentCard.gti")},
            }
            yield Listitem.from_dict(**item_data)

    def build_seasons(self, items):
        for each in items:
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_episodes"),
                "label": each.get("title"),
                "art": {"thumb": "", "fanart": ""},
                "params": {"id": deep_get(each, "value.data.widgetId")},
            }
            item = Listitem.from_dict(**item_data)
            item.art.local_thumb("season.png")
            yield item

    def build_item(self, items):
        for each in items:
            if each.get("type") == "DESCRIPTION_CARD":
                _, fanart = get_images(each)
                item_data = {
                    "callback": Resolver.ref("/resources/lib/main:play_video"),
                    "label": deep_get(each, "data.name"),
                    "art": {"thumb": fanart},
                    "info": {
                        "mpaa": deep_get(each, "data.regulatoryRating"),
                        "genre": deep_get(each, "data.genres"),
                        "plot": deep_get(each, "data.synopsis"),
                        "plotoutline": deep_get(each, "data.synopsis"),
                        "episode": deep_get(each, "data.episodeNumber"),
                        "duration": deep_get(each, "data.contentLengthInSeconds"),
                        "season": deep_get(each, "data.seasonNumber"),
                        "mediatype": deep_get(each, "data.vodType"),
                    },
                    "params": {"id": deep_get(each, "data.contentId")},
                }
                yield Listitem.from_dict(**item_data)

    def build_play(self, video, stream_headers):
        license_key = "|Content-Type=application/octet-stream|R{SSM}|"

        is_helper = inputstreamhelper.Helper("mpd", drm="com.widevine.alpha")

        if is_helper.check_inputstream():
            item_data = {
                "callback": deep_get(video, "data.playbackAssets.manifestURL"),
                "label": deep_get(video, "data.contentDetails.name"),
                "properties": {
                    "IsPlayable": True,
                    "inputstream": is_helper.inputstream_addon,
                    "inputstream.adaptive.manifest_type": "mpd",
                    "inputstream.adaptive.license_type": "com.widevine.alpha",
                    "inputstream.adaptive.stream_headers": urlencode(stream_headers),
                    "inputstream.adaptive.license_key": license_key,
                },
            }
            return Listitem(content_type="video").from_dict(**item_data)

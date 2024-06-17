from functools import reduce
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from codequick.script import Settings


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def update_query_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def get_images(item):
    img = deep_get(item, "data.imageSrc")
    return img, img


def get_deviceid():
    return Settings.get_string("device_id")

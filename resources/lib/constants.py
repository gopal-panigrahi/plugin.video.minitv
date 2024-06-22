from resources.lib.utils import get_deviceid
from codequick.utils import urljoin_partial

# URLs
CONTENT_BASE_URL = "https://www.amazon.in/minitv-op/api/web/"

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

DEVICE_ID = get_deviceid()

BASE_HEADERS = {
    "Accept": "application/json",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
    "Accounttype": "EXISTING_GUEST_ACCOUNT",
    "Atdevicetypeid": "A3EFOJ6EMJCZLM",
    "Cache-control": "no-cache",
    "Campaigntype": "DF_CP",
    "Currentpageurl": "/",
    "Currentplatform": "dWeb",
    "Deviceid": DEVICE_ID,
    "Devicetypeid": "A3EFOJ6EMJCZLM",
    "Isexternalcampaign": "false",
    "Operationname": "getPageLayout",
    "Pagedomain": "www.amazon.in",
    "Referer": "https://www.amazon.in/minitv",
    "Reftag": "avod_undef",
    "Rtt": "100",
    "Sec-Ch-Device-Memory": "8",
    "Sec-Ch-Dpr": "1",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Sec-Ch-Ua-Platform-Version": '"5.15.0"',
    "Sec-Ch-Viewport-Width": "1366",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": USER_AGENT,
}

url_constructor = urljoin_partial(CONTENT_BASE_URL)

MAIN_MENU = [
    ("Home", "home", "home.png"),
    ("Imported", "imported", "web.png"),
    ("Web Series", "web-series", "tv.png"),
    ("Playground", "playground", "show.png"),
    ("Movies", "movies", "movies.png"),
    ("Romance", "romance", "romance.png"),
    ("Comedy", "comedy", "comedy.png"),
]

URLS = {
    "PAGE": "page/storefront",
    "CONTENT": "page/title",
    "EPISODE": "widget",
}

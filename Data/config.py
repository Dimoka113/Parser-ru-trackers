import os, requests, re
from Data.api import COOKIES

BASE_URL = "https://rutracker.me/forum/"
TOPIC_URL = BASE_URL + "viewtopic.php?t=6579518"

limit = 100

POST_BODY_ID = "p-86768813"

SAVE_DIR = "torrents"
STATS_FILE = "Data/stats.json"
EXIST_JSON_FILE = "Data/check.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Referer": TOPIC_URL,}



TORRENT_ID_RE = re.compile(rb"viewtopic\.php\?t=(\d+)")
os.makedirs(SAVE_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)
NAME_RANGE = 50
FORUM_URL = "https://rutracker.me/forum/viewforum.php"

PAGE_SIZE = 50
MAX_PAGES = PAGE_SIZE * 10   # None = без лимита, иначе число страниц
SEEDS_LIMIT = 5
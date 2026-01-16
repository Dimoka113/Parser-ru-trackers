import os, requests, re
from Defs.api import Api

class Config(object):
    api: Api = None
    def __init__(self, api: Api):
        self.api = api
        self.session.cookies.update(self.api.COOKIES)
        os.makedirs(self.SAVE_DIR, exist_ok=True)

    session = requests.Session()
    BASE_URL = "https://rutracker.me/forum/"
    FORUM_URL = BASE_URL+ "viewforum.php"

    TOPIC_URL = str()
    SAVE_DIR = str()
    STATS_FILE = str()
    EXIST_JSON_FILE = str()
    HEADERS = dict()
    TORRENT_ID_RE = re.compile(rb"viewtopic\.php\?t=(\d+)")
    time_wait = 1
    NAME_RANGE = 50 # Лимит символов на файл торрента
    limit = 100 # Лимит файлов торрентов на один запуск
    PAGE_SIZE = 50
    MAX_PAGES = PAGE_SIZE * 10   # None = без лимита, иначе число страниц
    SEEDS_LIMIT = 5

    TOPIC_URL = BASE_URL + "viewtopic.php?t=6579518" 
    SAVE_DIR = "torrents"
    STATS_FILE = "Data/stats.json"
    EXIST_JSON_FILE = "Data/check.json"

    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Referer": TOPIC_URL,}

    POST_BODY_ID = "p-86768813"

    session.headers.update(HEADERS)

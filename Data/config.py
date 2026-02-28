import os, requests, re
from Defs.api import Api

class Config(object):
    api: Api = None
    BASE_URL = "https://rutracker.me/forum/"
    HEADERS = None
    session = requests.Session()

    def __init__(self, main_id_topic: int, api: Api):
        self.api = api
        self.session.cookies.update(self.api.COOKIES)
        os.makedirs(self.SAVE_DIR, exist_ok=True)
        TOPIC_URL = self.BASE_URL + f"viewtopic.php?t={str(main_id_topic)}" 
        self.HEADERS = {"User-Agent": self.api.UserAgent, "Referer": TOPIC_URL,}
        self.session.headers.update(self.HEADERS)

    REDBOOK_URL = BASE_URL + "viewtopic.php?t=6579518" 
    FORUM_URL = BASE_URL + "viewforum.php"
    SAVE_DIR = str()
    STATS_FILE = str()
    EXIST_JSON_FILE = str()
    TORRENT_ID_RE = re.compile(rb"viewtopic\.php\?t=(\d+)")
    NAME_RANGE = 50 # Лимит символов на файл торрента
    limit = 0
    PAGE_SIZE = 50
    MAX_PAGES = PAGE_SIZE * 10   # None = без лимита, иначе число страниц
    SEEDS_LIMIT = 0 # (<= Сидов)
    SAVE_DIR = "torrents"
    STATS_FILE = "Data/stats.json"
    EXIST_JSON_FILE = "Data/check.json"
    POST_BODY_ID = "p-86768813"


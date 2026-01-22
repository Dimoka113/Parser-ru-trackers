import requests
import datetime
import json
from typing import Any
from threading import Thread
import time
import pickle
from Defs.rutracker import RuTracker
from Data.config import Config
from Defs.api import Api
from requests.auth import HTTPBasicAuth
from Defs.logger import Logger


class Call(object):
    try_limit = 5
    log: Logger = Logger("Caller")

    def _get(self, path: str) -> Any:
        url = f"{self.url}{path}"
        sleep = 0.5
        for _ in range(self.try_limit+1):
            try:
                r = self.s.get(url, timeout=10)
                if r.status_code == 200:
                    return r.json()
                last_error = f"HTTP {r.status_code}: {r.text}"
            except (requests.RequestException, ValueError) as e:
                last_error = str(e)
            time.sleep(sleep)
            sleep = sleep + 0.5
        self.log.warn(f"[!] GET {path} ошибка после 5 попыток: {last_error}")
        return None


    def _post(self, path: str, data: dict):
        url = f"{self.url}{path}"
        sleep = 0.5
        for _ in range(self.try_limit+1):
            try:
                r = self.s.post(url, data=data, timeout=10)
                if r.status_code == 200:
                    return r.text
                last_error = f"HTTP {r.status_code}: {r.text}"
            except requests.RequestException as e:
                last_error = str(e)
            time.sleep(sleep)
            sleep = sleep + 0.5
        self.log.warn(f"[!] POST {path} ошибка после 5 попыток: {last_error}")
        return None



class Qbit(Call):
    url = str()
    s = requests.Session()
    path_to_cokkies = str()
    api = Api()
    httpBA = None
    rutracker: RuTracker = None
    cfg: Config = None
    log: Logger = Logger("Qbit")

    def __init__(self, FOR_ID: int, httpBA: HTTPBasicAuth = None, path_to_cokkies: str = "Data/qbit.cokkies.pkl"):
        self.url = self.api.url
        self.path_to_cokkies = path_to_cokkies
        self.httpBA = httpBA
        self.cfg = Config(FOR_ID, self.api)
        self.rutracker = RuTracker(self.cfg)
        self.log.debug(self.cfg.HEADERS)


    def auth(self, username: str, password: str, path="/api/v2/auth/login"):
        self.s.auth = self.httpBA
        r = self._post(path, data={"username": username, "password": password})

    def save_cokkies(self, path_to_cokkies: str):
        with open(path_to_cokkies, "wb") as f:
            pickle.dump(self.s.cookies, f)



    def version(self, path="/api/v2/app/version"):
        return self._get(path)
        
    def get_torrents(self, path=f"/api/v2/sync/maindata?{datetime.datetime.now().strftime('%d%m%Y%H%M%S')}"):
        return self._get(path)

    def get_torrents_ids(self, path=f"/api/v2/sync/maindata?{datetime.datetime.now().strftime('%d%m%Y%H%M%S')}") -> list[str]:
        return [i for i in self._get(path)["torrents"]]

    def get_torrent_trackers(self, hah, path="/api/v2/torrents/trackers?hash={hah}"):
        return self._get(path.format(hah=hah))

    def get_torrent(self, hah, path="/api/v2/torrents/properties?hash={hah}"):
        return self._get(path.format(hah=hah))
    
    def add_tags(self, tags: list[str], hashes: list[str], path="/api/v2/torrents/addTags"):
        return self._post(path, data={"tags": tags, "hashes": hashes})

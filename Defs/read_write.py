import os, json
from Data.config import Config


class RW(object):
    cfg: Config = None
    def __init__(self, cfg: Config):
        self.cfg = cfg


    def append_ids_to_json(self, uid: int):
        if not os.path.exists(self.cfg.EXIST_JSON_FILE):
            with open(self.cfg.EXIST_JSON_FILE, "w+", encoding="utf-8") as f:
                json.dump([], f, indent=3)

        with open(self.cfg.EXIST_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if uid in data:
            return False
        else:
            data.append(uid)
            with open(self.cfg.EXIST_JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(sorted(data), f, indent=3)
            return True


    def load_ids_from_json(self):
        if not os.path.exists(self.cfg.EXIST_JSON_FILE):
            return list()

        with open(self.cfg.EXIST_JSON_FILE, "r", encoding="utf-8") as f:
            return list(json.load(f))
        

    def white_check(self, stats):
        with open(self.cfg.STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=3)
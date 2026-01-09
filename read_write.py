import os, json
from Data.config import STATS_FILE, EXIST_JSON_FILE

def append_ids_to_json(uid: int):
    if not os.path.exists(EXIST_JSON_FILE):
        with open(EXIST_JSON_FILE, "w+", encoding="utf-8") as f:
            json.dump([], f, indent=3)

    with open(EXIST_JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if uid in data:
        return False
    else:
        data.append(uid)
        with open(EXIST_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(data), f, indent=3)
        return True


def load_ids_from_json():
    if not os.path.exists(EXIST_JSON_FILE):
        return list()

    with open(EXIST_JSON_FILE, "r", encoding="utf-8") as f:
        return list(json.load(f))
    

def white_check(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=3)
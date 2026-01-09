import json
from Data.config import *
from defs import *
from read_write import *


def main(only_check=False, custom_post=None):

    if only_check:
        summ = 0
        existing_ids = load_existing_torrent_ids()
        print(f"Уже есть торрентов: {len(existing_ids)}")
        for i in existing_ids:
            if append_ids_to_json(int(i)):
                summ += 1

        print(f"Добавлено в json {summ} торрентов")
        return

    if custom_post is not None:
        topic_ids = custom_post
        print(f"Используется custom_post, тем: {len(topic_ids)}")
    else:
        topic_ids = get_topic_ids()
        print(f"Найдено тем: {len(topic_ids)}", f"Лимит трекеров: {limit}")

    existing_ids = load_existing_torrent_ids()
    print(f"Уже есть торрентов в директории: {len(existing_ids)}")

    jsondata = load_ids_from_json()
    print(f"Уже есть торрентов в json: {len(jsondata)}")

    data = set(map(int, jsondata)) | set(map(int, existing_ids))

    done = 1
    stats = []

    for tid in topic_ids:
        tid = int(tid)

        if tid in data:
            print(f"[=] {tid} уже есть — пропуск")
            continue
        if limit and done > limit:
            break
        try:
            info = parse_topic_page(tid)
            ok = download_torrent(tid, info["name"])
            if ok:
                stats.append({
                    tid: {
                        "name": info["name"],
                        "seeds": info["seeds"],
                        "leech": info["leech"],
                        "stat": info["stat"],
                    }
                })
                white_check(stats)
                append_ids_to_json(tid)
                print(f"[+] {tid} OK")
                done += 1
            else:
                print(f"[!] {tid} пропущен")
        except Exception as e:
            print(f"[!] {tid} ошибка: {e}")

if __name__ == "__main__":
    FORUM_ID = 54
    low_seed_ids = get_low_seed_topic_ids(FORUM_ID)
    print(f"Найдено тем с сидами < {SEEDS_LIMIT}: {len(low_seed_ids)}")
    main(False, low_seed_ids) # Если истина, только проверка и добавление уже существуюзих торрентов в json

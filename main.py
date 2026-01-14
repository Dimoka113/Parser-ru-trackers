import json
from Data.config import *
from Defs.qofflife import *
from Defs.read_write import *
from Defs.qbit import Qbit


if __name__ == "__main__":
    qbit = Qbit()
    FORUM_ID = 0
    check = False # Если истина, только проверка и добавление уже существуюзих торрентов в json
    if not check and FORUM_ID != 0:
        low_seed_ids = qbit.rutracker.get_low_seed_topic_ids(FORUM_ID)
        print(f"Найдено тем с сидами < {qbit.cfg.SEEDS_LIMIT}: {len(low_seed_ids)}")
        qbit.rutracker.main(check, low_seed_ids, 0) 
    else:
        qbit.rutracker.main(check)



# Пример использования класса Qbit, для проверки "актуальности трекера"
# В будующем весь проект перейдёт в класс qbit, и будет не актуально.
# def trackers(i: str):
#     for x in qb.get_torrent_trackers(i):
#         if x["status"] != 2:
#             gt = qb.get_torrent(i)
#             print(i, x["status"], x["msg"], gt["comment"])
#             print(qb.add_tags(["Стоят"], [i]))
#         else:
#             print(f"[{i}] Всё ок")

# for i in qb.get_torrents_ids():
#     s = Thread(target=trackers, args=(i,),)
#     s.start()
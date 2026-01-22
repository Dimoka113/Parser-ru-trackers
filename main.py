import json
from Data.config import *
from Defs.qofflife import *
from Defs.read_write import *
from Defs.qbit import Qbit
from Defs.logger import Logger

Logger.level(Logger.types.DEBUG)

if __name__ == "__main__":
    FORUM_ID = 0 # Айди форума, откуда парсить торренты (если 0, используется альтернативная схема для "красной книги")
    download_limit = 0 # Лимит размера конечного торрента (в байтах)
    
    log = Logger("Main"); qbit = Qbit(FORUM_ID)
    check = False # Если истина, только проверка и добавление уже существуюзих торрентов в json
    if not check and FORUM_ID != 0:
        low_seed_ids = qbit.rutracker.get_low_seed_topic_ids(FORUM_ID)
        log.debug(f"Найдено тем с сидами < {qbit.cfg.SEEDS_LIMIT}: {len(low_seed_ids)}")
        qbit.rutracker.main(check, low_seed_ids, download_limit=download_limit) 
    else:
        qbit.rutracker.main(check, download_limit=download_limit)



# Пример использования класса Qbit, для проверки "актуальности трекера"
# В будующем весь проект перейдёт в класс qbit, и будет не актуально.
# def trackers(i: str):
#     for x in qb.get_torrent_trackers(i):
#         if x["status"] != 2:
#             gt = qb.get_torrent(i)
#             self.log.info(i, x["status"], x["msg"], gt["comment"])
#             self.log.info(qb.add_tags(["Стоят"], [i]))
#         else:
#             self.log.info(f"[{i}] Всё ок")

# for i in qb.get_torrents_ids():
#     s = Thread(target=trackers, args=(i,),)
#     s.start()
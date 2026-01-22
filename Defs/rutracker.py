import os, re
from bs4 import BeautifulSoup
from Data.config import Config
from Defs.qofflife import *
from Defs.read_write import *
from Defs.logger import Logger


class RuTracker(object):
    cfg: Config = None
    rw: RW = None
    log: Logger = Logger("RuTracker")

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.rw = RW(cfg)


    def main(self, only_check=False, custom_post=None, download_limit: int = 0):
        if only_check:
            summ = 0
            existing_ids = self.load_existing_torrent_ids()
            self.log.debug(f"Уже есть торрентов: {len(existing_ids)}")
            for i in existing_ids:
                if self.rw.append_ids_to_json(int(i)):
                    summ += 1

            self.log.debug(f"Добавлено в json {summ} торрентов")
            return

        if custom_post is not None:
            topic_ids = custom_post
            self.log.debug(f"Используется custom_post, тем: {len(topic_ids)}")
        else:
            topic_ids = self.get_topic_ids()
            self.log.info(f"Найдено тем: {len(topic_ids)}", f"Лимит трекеров: {self.cfg.limit}")

        existing_ids = self.load_existing_torrent_ids()
        self.log.debug(f"Уже есть торрентов в директории: {len(existing_ids)}")

        jsondata = self.rw.load_ids_from_json()
        self.log.debug(f"Уже есть торрентов в json: {len(jsondata)}")

        data = set(map(int, jsondata)) | set(map(int, existing_ids))

        done = 1
        stats = []
        
        if len(topic_ids) == 0:
            self.log.crit("Не найдено тем!")
            return False

        for tid in topic_ids:
            tid = int(tid)

            if tid in data:
                self.log.debug(f"[=] {tid} уже есть — пропуск")
                continue
            if self.cfg.limit and done > self.cfg.limit:
                break
            try:
                info = self.parse_topic_page(tid)
                if download_limit == 0 or float(info["size"]) < download_limit:
                    ok = self.download_torrent(tid, info["name"])
                    if ok:
                        stats.append({
                            tid: {
                                "name": info["name"],
                                "seeds": info["seeds"],
                                "leech": info["leech"],
                                "stat": info["stat"],
                                "size": info["size_str"]
                            }
                        })
                        self.rw.white_check(stats)
                        self.rw.append_ids_to_json(tid)
                        self.log.info(f"[+] {tid} OK")
                        done += 1

                    else:
                        self.log.warn(f"[!] {tid} пропущен!")
                else:
                    self.log.debug(f"[*!] {tid} Слишком большой." + f" ({info['size_str']})")
                    
            except Exception as e:
                self.log.warn(f"[!] {tid} ошибка: {e}")

    def load_existing_torrent_ids(self):
        ids = set()

        for fname in os.listdir(self.cfg.SAVE_DIR):
            if not fname.endswith(".torrent"):
                continue

            path = os.path.join(self.cfg.SAVE_DIR, fname)
            try:
                with open(path, "rb") as f:
                    data = f.read()

                m = self.cfg.TORRENT_ID_RE.search(data)
                if m:
                    ids.add(m.group(1).decode())
            except Exception:
                pass

        return list(ids)


    def get_topic_ids(self):
        r = self.cfg.session.get(self.cfg.TOPIC_URL)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        post_body = soup.find("div", class_="post_body", id=self.cfg.POST_BODY_ID)

        if not post_body:
            raise RuntimeError("post_body не найден")

        ids = []
        for a in post_body.find_all("a", class_="postLink", href=True):
            m = re.search(r"viewtopic\.php\?t=(\d+)", a["href"])
            if m:
                ids.append(m.group(1))

        return sorted(set(ids))




    def parse_topic_page(self, topic_id):
        url = self.cfg.BASE_URL + f"viewtopic.php?t={topic_id}"
        r = self.cfg.session.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")


        title_tag = soup.find("a", id="topic-title")
        name = title_tag.get_text(strip=True) if title_tag else f"topic_{topic_id}"

        def extract_int(selector):
            tag = soup.select_one(selector)
            if not tag:
                return None
            b = tag.find("b")
            return int(b.text) if b and b.text.isdigit() else None

        seeds = extract_int("span.seed")
        leech = extract_int("span.leech")

        stat_td = soup.find("td", class_="borderless")
        data = str(stat_td.get_text(" ", strip=True)).replace(" ", " ")

        if data:
            size = data.split("Размер: ")[1].split(" |")[0]
            stat = data.split("\n\t\t")[1]


            return {"id": topic_id, "name": name, "seeds": seeds, "leech": leech, "size": parse_data_size(size), "size_str": size, "stat": stat}
        else:
            return {"id": topic_id,"name": name,"seeds": seeds,"leech": leech,}


    def download_torrent(self, topic_id, name):
        safe_name = re.sub(r'[\\/*?:"<>|]', "_", name)
        filename = f"{safe_name[0:self.cfg.NAME_RANGE]} (rutracker-{topic_id}).torrent"
        path = os.path.join(self.cfg.SAVE_DIR, filename)

        url = self.cfg.BASE_URL + f"dl.php?t={topic_id}"
        r = self.cfg.session.get(url)

        if r.headers.get("Content-Type", "").startswith("text/html"):
            self.log.warn(f"[!] {topic_id}: не торрент")
            return False

        with open(path, "wb") as f:
            f.write(r.content)

        return True


    def get_topics_from_forum(self, url: str):
        r = self.cfg.session.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        tbody = soup.find("tbody")

        if not tbody:
            raise RuntimeError("tbody не найден")

        topics = []

        for tr in tbody.find_all("tr", id=re.compile(r"^tr-\d+")):
            topic_id = tr.get("data-topic_id")
            if not topic_id:
                continue

            # сиды
            seed_td = tr.find("td", class_="seedmed") or tr.find("td", class_="seed")
            seeds = None

            if seed_td:
                try:
                    seeds = int(seed_td.get_text(strip=True))
                except ValueError:
                    seeds = None

            topics.append({
                "id": topic_id,
                "seeds": seeds,
            })

        return topics


    def extract_counter(self, tr, classes):
        span = tr.find("span", class_=classes)
        if not span:
            return None

        b = span.find("b")
        if not b:
            return None

        txt = b.get_text(strip=True)
        return int(txt) if txt.isdigit() else None


    def parse_forum_page(self, forum_id, start=0):
        params = {"f": forum_id,"start": start}
        r = self.cfg.session.get(self.cfg.FORUM_URL, params=params)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table",class_="vf-table vf-tor forumline forum")

        if not table:
            self.log.crit(f"[!] Таблица форума не найдена (start={start})"); return []
        topics = []

        for tr in table.find_all("tr", id=re.compile(r"^tr-\d+")):
            topic_id = tr.get("data-topic_id")
            if not topic_id: continue

            seeds = self.extract_counter(tr, ["seed", "seedmed", "seedbg"])
            leech = self.extract_counter(tr, ["leech", "leechmed"])
            topics.append({"id": int(topic_id),"seeds": seeds,"leech": leech,})

        return topics

    def get_subforums(self, forum_id: int):
        r = self.cfg.session.get(self.cfg.FORUM_URL, params={"f": forum_id})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        subforums = []
        for h4 in soup.find_all("h4", class_="forumlink"):
            a = h4.find("a", href=True)
            if not a:
                continue
            m = re.search(r"viewforum\.php\?f=(\d+)", a["href"])
            if m:
                subforums.append(int(m.group(1)))
        return list(set(subforums))

    def iter_forum_topics(self, forum_id):
        seen = set()
        page = 0

        while True:
            if self.cfg.MAX_PAGES is not None and page >= self.cfg.MAX_PAGES: break
            start = page + self.cfg.PAGE_SIZE
            topics = self.parse_forum_page(forum_id, start=start)
            if not topics: break
            new_on_page = 0

            for t in topics:
                if t["id"] in seen: continue
                seen.add(t["id"])
                new_on_page += 1
                yield t

            if new_on_page == 0: break
            page += self.cfg.PAGE_SIZE
            
    def iter_forum_topics_recursive(self, forum_id: int, visited_forums=None):
        if visited_forums is None:
            visited_forums = set()

        if forum_id in visited_forums:
            return

        visited_forums.add(forum_id)
        self.log.debug(f"[->] Обход форума: {forum_id}")

        for topic in self.iter_forum_topics(forum_id):
            yield topic

        try:
            subforums = self.get_subforums(forum_id)
        except Exception as e:
            self.log.warn(f"[!] Не удалось получить подфорумы f={forum_id}: {e}")
            return

        for sub_id in subforums:
            yield from self.iter_forum_topics_recursive(
                sub_id,
                visited_forums
            )

    def get_low_seed_topic_ids(self, forum_id):
        ids = []

        for topic in self.iter_forum_topics_recursive(forum_id):
            seeds = topic["seeds"]
            if seeds is None: continue
            if seeds < self.cfg.SEEDS_LIMIT: ids.append(topic["id"])
        return ids
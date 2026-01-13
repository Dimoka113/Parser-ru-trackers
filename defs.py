import os
from Data.config import *
from bs4 import BeautifulSoup

def parse_data_size(string: str) -> int:
    size, datatype = string.split(" ")

    if datatype == "TB": return float(size) * 1024 * 1024 * 1024 * 1024
    elif datatype == "GB": return float(size) * 1024 * 1024 * 1024
    elif datatype == "MB": return float(size) * 1024 * 1024
    elif datatype == "KB": return float(size) * 1024 * 1024
    elif datatype == "B": return float(size)
    else: raise Exception("Неизвестный тип данных!")


def load_existing_torrent_ids():
    ids = set()

    for fname in os.listdir(SAVE_DIR):
        if not fname.endswith(".torrent"):
            continue

        path = os.path.join(SAVE_DIR, fname)
        try:
            with open(path, "rb") as f:
                data = f.read()

            m = TORRENT_ID_RE.search(data)
            if m:
                ids.add(m.group(1).decode())
        except Exception:
            pass

    return list(ids)


def get_topic_ids():
    r = session.get(TOPIC_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    post_body = soup.find("div", class_="post_body", id=POST_BODY_ID)

    if not post_body:
        raise RuntimeError("post_body не найден")

    ids = []
    for a in post_body.find_all("a", class_="postLink", href=True):
        m = re.search(r"viewtopic\.php\?t=(\d+)", a["href"])
        if m:
            ids.append(m.group(1))

    return sorted(set(ids))




def parse_topic_page(topic_id):
    url = BASE_URL + f"viewtopic.php?t={topic_id}"
    r = session.get(url)
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


def download_torrent(topic_id, name):
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", name)
    filename = f"{safe_name[0:NAME_RANGE]} (rutracker-{topic_id}).torrent"
    path = os.path.join(SAVE_DIR, filename)

    url = BASE_URL + f"dl.php?t={topic_id}"
    r = session.get(url)

    if r.headers.get("Content-Type", "").startswith("text/html"):
        print(f"[!] {topic_id}: не торрент")
        return False

    with open(path, "wb") as f:
        f.write(r.content)

    return True


def get_topics_from_forum(url: str):
    r = session.get(url)
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


def extract_counter(tr, classes):
    span = tr.find("span", class_=classes)
    if not span:
        return None

    b = span.find("b")
    if not b:
        return None

    txt = b.get_text(strip=True)
    return int(txt) if txt.isdigit() else None


def parse_forum_page(forum_id, start=0):
    params = {"f": forum_id,"start": start}
    r = session.get(FORUM_URL, params=params)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table",class_="vf-table vf-tor forumline forum")

    if not table:
        print(f"[!] Таблица форума не найдена (start={start})"); return []
    topics = []

    for tr in table.find_all("tr", id=re.compile(r"^tr-\d+")):
        topic_id = tr.get("data-topic_id")
        if not topic_id: continue

        seeds = extract_counter(tr, ["seed", "seedmed", "seedbg"])
        leech = extract_counter(tr, ["leech", "leechmed"])
        topics.append({"id": int(topic_id),"seeds": seeds,"leech": leech,})

    return topics

def iter_forum_topics(forum_id):
    seen = set()
    page = 0

    while True:
        if MAX_PAGES is not None and page >= MAX_PAGES: break
        start = page + PAGE_SIZE
        topics = parse_forum_page(forum_id, start=start)
        if not topics: break
        new_on_page = 0

        for t in topics:
            if t["id"] in seen: continue
            seen.add(t["id"])
            new_on_page += 1
            yield t

        if new_on_page == 0: break
        page += PAGE_SIZE

def get_low_seed_topic_ids(forum_id):
    ids = []

    for topic in iter_forum_topics(forum_id):
        seeds = topic["seeds"]
        if seeds is None: continue
        if seeds < SEEDS_LIMIT: ids.append(topic["id"])
    return ids
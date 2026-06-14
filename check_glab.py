import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://honyaku.kitsune-bdojp.workers.dev/?url=https://blackdesert.pearlabyss.com/GlobalLab/en-US/News/Notice?_categoryNo=2"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

article = soup.select_one("ul.board_list li a.board_item_inner")

if article is None:
    raise Exception("記事取得失敗")

board_no = article.get("data-boardno")
link = article.get("href")

title_tag = article.select_one("p.title.line_clamp")
title = title_tag.get_text(strip=True) if title_tag else "タイトル取得失敗"

current = {
    "board_no": board_no,
    "link": link,
    "title": title
}

STATE_FILE = "state_glab.json"

if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        old = json.load(f)
else:
    old = {}

if old.get("board_no") != board_no:

    requests.post(
        os.environ["DISCORD_WEBHOOK_2"],
        json={
            "content":
            f"🧪 Global Lab更新\n"
            f"【{title}】\n\n"
            f"🇯🇵 日本語翻訳\n{link}"
        }
    )

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False)

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

print("board_no =", board_no)
print("title =", title)
print("link =", link)

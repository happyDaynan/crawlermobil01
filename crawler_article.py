import requests
import os
import json
import collections
import re
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pymongo import MongoClient


conn_path = "./conn_info.txt"
with open(conn_path, "r") as f:
    a = json.loads(f.read())


engine = create_engine(
    f"mysql+pymysql://{a['mysql'][0]}:{a['mysql'][1]}@{a['mysql'][2]}/{a['mysql'][3]}"
)
cnx = engine.connect()

select_query = cnx.execute("SELECT href FROM brand_href")

url_list = ["https://www.mobile01.com/" + i[0] for i in select_query]


ua = UserAgent()
ua = ua.random

dict_list = []
headers = {"user-agent": ua}
for url in url_list:

    try:
        res = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    soup = BeautifulSoup(res.text, "lxml")
    # 文章標題
    title = soup.find_all("h1", class_="t2")[0].text
    re_title = "".join(i for i in re.findall(r"[\u4e00-\u9fa5\w]+", title))
    title = re_title

    # 發文時間
    article_time = soup.find_all("span", class_="o-fNotes o-fSubMini")[0].text

    # 瀏覽人數
    visitors = soup.find_all("span", class_="o-fNotes o-fSubMini")[1].text

    # 讚數
    likes = soup.find_all("span", class_="o-fSubMini")[6].text

    # 針對文章內容作處理
    # 文章內容
    articleBody = soup.find_all("div", class_="u-gapNextV--md")[0].text
    # 拿掉網址
    re_articleBody = re.sub(
        r"^https?:\/\/.*[\r\n]*", "", articleBody, flags=re.MULTILINE
    )
    # 清除\n\r
    re_articleBody = re.sub(r"[\n\r]+", "", re_articleBody, flags=re.MULTILINE)
    # 取出中文及英文
    re_articleBody = "".join(
        i for i in re.findall(r"[\u4e00-\u9fa5\w]+", re_articleBody)
    )

    # 一篇文章整理成字典
    article_dict = {
        "title": title,
        "article_time": article_time,
        "visitors": visitors,
        "likes": likes,
        "articleBody": re_articleBody,
        "url": url,
    }
    dict_list.append(article_dict)

    if len(dict_list) == 100:
        # 建立連線
        # mongodb://users:password@your_ip/db_name.collection_name
        client = MongoClient(
            f"mongodb://{a['mongodb'][0]}:{a['mongodb'][1]}@{a['mongodb'][2]}"
        )
        if f"{a['mongodb'][3]}" in client.list_database_names():

            db = client[f"{a['mongodb'][3]}"]
            collection = db[f"{a['mongodb'][4]}"]
            collection.insert_many(dict_list)
            dict_list = []
    else:
        pass

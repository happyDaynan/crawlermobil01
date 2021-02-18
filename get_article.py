from pymongo import MongoClient
from elasticsearch import Elasticsearch
from datetime import datetime
import json, os, jieba

conn_path = "./conn_info.txt"
with open(conn_path, 'r') as f:
    a = json.loads(f.read())

path = "./Brand_name.txt"
with open(path, 'r') as f:
    car_num = json.loads(f.read())

# 設定繁體字典檔
jieba.set_dictionary('./dict/dict.txt.big')
# 設定使用者自訂字典
jieba.load_userdict('./dict/car_dict.txt')


client = MongoClient(f"mongodb://{a['mongodb'][0]}:{a['mongodb'][1]}@{a['mongodb'][2]}")

db = client[f"{a['mongodb'][3]}"]
collection = db[f"{a['mongodb'][4]}"]

for x in collection.find():
    brand_num = x['url'].split('f=')[1].split('&')[0]
    # 品牌代碼轉換
    for c in car_num:
        for brand, num in car_num[c].items():
            if brand_num == num:
                brand_name = brand
    # 字串轉日期時間
    article_time = datetime.strptime(x['article_time'], "%Y-%m-%d %H:%M%S")
    # 取得現在時間
    now_time = datetime.now()
    # 針對文章內容做斷字斷詞
    reg_article = " ".join(jieba.cut(x['articleBody'], cut_all=False, HMM=True))
    
    









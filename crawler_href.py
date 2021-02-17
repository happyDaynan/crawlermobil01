import requests, os, json, collections
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
from datetime import datetime
from sqlalchemy import create_engine


path = "./Brand_name.txt"
with open(path, 'r') as f:
    car_num = json.loads(f.read())


ua = UserAgent()
ua = ua.random
headers = {'user-agent': ua}

article_dict = collections.defaultdict(list)
for country in car_num:
    for brand in car_num[country]:
        # 找出最後一頁
        url =  f"https://www.mobile01.com/topiclist.php?f={car_num[country][brand]}"
        
        res = requests.get(url, headers= headers)
        soup =  BeautifulSoup(res.text, 'lxml')
        p = soup.find_all('ul', class_='l-pagination')[0]
        maxpage = []
        for i in p :
            if i.text != "":
                maxpage.append(int(i.text))
        last_pages = max(maxpage)
        # 找出所有文章連結
        pages = 1
        while pages <= last_pages:
            headers = {'user-agent': ua}
            page_url = url + f"&p={pages}"

            try: 
                res = requests.get(page_url, headers=headers)
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)

            soup =  BeautifulSoup(res.text, 'lxml')
            
            for a in soup.find_all('a', class_='c-link u-ellipsis'):
                if len(a.get('href').split("&t=")) == 2:
                    article_dict['article_id'].append(str(a.get('href').split("&t=")[1]))
                    article_dict['country'].append(country)
                    article_dict['brand'].append(car_num[country][brand])                      
                    article_dict['href'].append(str(a.get('href')))
                    article_dict['todbtime'].append(datetime.now().strftime('%Y-%m-%d'))
                else:
                    break
            pages += 1
            
df = pd.DataFrame.from_dict(article_dict)
# 設定文章爬取狀態
df["articletype"] = "0"
# 清除重覆資料
df = df.drop_duplicates(subset='article_id', keep='first', inplace=False)
# print(df)           



conn_path = "./conn_info.txt"
with open(conn_path, 'r') as f:
    a = json.loads(f.read())


engine = create_engine(f"mysql+pymysql://{a['mysql'][0]}:{a['mysql'][1]}@{a['mysql'][2]}/{a['mysql'][3]}")
cnx = engine.connect()
df.to_sql("brand_href", cnx, index=False, if_exists="append")
cnx.close()

    


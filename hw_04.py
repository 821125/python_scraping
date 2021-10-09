import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint

# to create data base and connect to Mongo DB
client = MongoClient('localhost', 27017)
db = client['db_news']
base = db.news  # to create collection

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/93.0.4577.82 Safari/537.36'}

response = requests.get('http://yandex.ru/news', headers=header)
items = html.fromstring(response.text).xpath("//article[contains(@class, 'mg-card')]")
all_news = []

for item in items:

    news = {
        'source': item.xpath(".//a[@class = 'mg-card__source-link']/text()"),  # source name
        'name': str(item.xpath(".//hz[@class = 'mg-card__title']/text()")).replace("\\xa0", " "),  # news name
        'link': item.xpath(".//a[@class = 'mg-card__link']/@href"),  # news link
        'time': item.xpath(".//span[@class = 'mg-card-source__time']/text()")  # time of publication
    }

    all_news.append(news)

    try:
        base.update_one({'link': news['link']}, {'$set': news}, upsert=True)
    except Exception as exc:
        print('we have some problem/n', exc)
        continue

    pprint(all_news)

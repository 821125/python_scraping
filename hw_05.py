from selenium import webdriver
from selenium.common import exceptions as se
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pprint import pprint
import time

client = MongoClient('127.0.0.1', 27017)
db = client['db_mail']
base = db.letters

chrome_options = Options()
chrome_options.add_argument('start_maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

elem = driver.find_element(By.NAME, "login")
elem.send_keys("study.ai_172@mail.ru")
elem.send_keys(Keys.ENTER)
time.sleep(5)
elem = driver.find_element(By.NAME, "password")
elem.send_keys("NextPassword172???")
elem.send_keys(Keys.ENTER)
time.sleep(10)

hrefs = []

while True:
    try:
        items = driver.find_elements(By.XPATH, "//a[contains(@class, 'letter')]")
        for item in items:
            hrefs.append(item.get_attribute('href'))
        item.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    except se.ElementNotInteractableException:
        break

hrefs = set(hrefs)
all_letters = []

for href in hrefs:
    driver.get(href)
    time.sleep(3)
    letters = {}
    correspondent = driver.find_element(By.XPATH, ".//span[@class = 'letter-contact']").text
    item_date = driver.find_element(By.XPATH, ".//div[@class = 'letter__date']").text
    theme = driver.find_element(By.XPATH, ".//h2[@class = 'thread__subject']").text
    content = driver.find_element(By.XPATH, "//div[@class = 'letter-body__body']").text

    letters['correspondent'] = correspondent
    letters['item_date'] = item_date
    letters['theme'] = theme
    letters['content'] = content
    letters['link'] = href
    all_letters.append(letters)

    try:
        base.update_one({'link': letters['link']}, {'$set': letters}, upsert=True)
    except Exception as exc:
        print('something wrong', exc)
        continue

pprint(all_letters)

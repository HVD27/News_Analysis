import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import pandas as pd


driver = uc.Chrome()
url = 'https://www.reddit.com/r/india/comments/18xp17c/given_the_role_of_us_in_blatantly_supporting/'

# print(url.split("/")[-3])
driver.get(url)
input('Please login to continue: ')
time.sleep(10)
# r= requests.get('https://www.reddit.com/r/india/comments/18xe0ay/gujarat_passengers_on_dunki_flight_had_offered_rs/')
s = BeautifulSoup(driver.page_source,'html.parser')

# title = s.select_one(f'#post-title-t3_{url.split("/")[-3]}').text.strip()
title = s.find('h1').text.strip()
print(title)
comment = '\n'.join([item.text.strip() for item in s.select_one('._1ump7uMrSA43cqok14tPrG').select('._3sf33-9rVAO_v4y0pIW_CH')])
data = {
    'title':title,
    'Comment':comment
}

df = pd.DataFrame([data])
df.to_csv('data10.csv')
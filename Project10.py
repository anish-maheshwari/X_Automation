from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from datetime import datetime

import sys
import io

# Set stdout to utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


import time

client = MongoClient('mongodb://localhost:27017')
db = client['twitter_trends']
collection = db['trends_data']


email = 'fewaja3431@cctoolz.com'
username = 'mehtaistesting'
password = 'test@123'

driver = webdriver.Chrome()


driver.get("https://x.com/?lang=en")
time.sleep(4)

 
element = driver.find_element(By.CSS_SELECTOR,'#react-root > div > div > div.css-175oi2r.r-1f2l425.r-13qz1uu.r-417010 > main > div > div > div.css-175oi2r.r-tv6buo.r-791edh.r-1euycsn > div.css-175oi2r.r-1777fci.r-nsbfu8.r-1qmwkkh > div > div.css-175oi2r > div.css-175oi2r.r-2o02ov > a > div > span > span')
                                          
element.click()
time.sleep(6)

userElement = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input')
                                           
userElement.send_keys(username)
time.sleep(1)
userElement.send_keys(Keys.RETURN)
time.sleep(2)
passElement = driver.find_element(By.XPATH,'//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
                                           
passElement.send_keys(password)
time.sleep(2)
passElement.send_keys(Keys.RETURN)
time.sleep(7)

showMore = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section/div/div/div[8]/div/a/div/span')
driver.execute_script("arguments[0].scrollIntoView(true);", showMore)

time.sleep(2)
showMore.click()
time.sleep(4)

trends = driver.find_elements(By.XPATH,"//*[contains(@id,'id__')]/div[2]/span") 

  # Ensure that we don't exceed the number of available trends
trend_names = []
for trend in trends[:min(5, len(trends))]:  # Ensure we only loop through the minimum of 5 or available trends
    trend_names.append(trend.text)


print(trend_names) 
  

# Check the current IP address


driver.get("https://httpbin.org/ip")
time.sleep(2)


# Get and print the current IP address
ip_element = driver.find_element(By.TAG_NAME, "pre")
print("Current IP Address:", ip_element.text)
ip_address = ip_element.text
time.sleep(8)
data = {
    "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "trends": trend_names,
    "ip_address": ip_address
}

collection.insert_one(data)

# Clean up
driver.quit()
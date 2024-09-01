from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

result_sentimate = 0
comment_count = 0

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=chrome_options)

video_url = "https://www.youtube.com/watch?v=Gx5qb1uHss4"
driver.get(video_url)

driver.execute_script(
    "window.scrollTo(0, document.documentElement.scrollHeight);")
time.sleep(3)

SCROLL_PAUSE_TIME = 3

last_height = driver.execute_script(
    "return document.documentElement.scrollHeight")

while True:
    driver.execute_script(
        "window.scrollTo(0, document.documentElement.scrollHeight);")

    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script(
        "return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

comments = driver.find_elements(By.CSS_SELECTOR, "#content-text")

all_comments = []

for comment in comments:
    all_comments.append(comment.text)

driver.quit()

for comment in all_comments:
    blob = TextBlob(comment)
    result_sentimate += blob.sentiment.polarity
    comment_count += 1

if result_sentimate/comment_count > 5:
    print("Vary Positive", result_sentimate/comment_count)
elif result_sentimate/comment_count > 0:
    print("Positive", result_sentimate/comment_count)
elif result_sentimate/comment_count < -5:
    print("Vary Negative", result_sentimate/comment_count)
elif result_sentimate/comment_count < 0:
    print("Negative", result_sentimate/comment_count)
else:
    print("Neutral")

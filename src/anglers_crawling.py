import os
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# 日付を設定
def set_date(driver, startYmd, endYmd):
    driver.find_element(By.CSS_SELECTOR,'span[style="display: inline-block;"] > button').click()
    sleep(3)

    date_start_box = driver.find_element(By.CSS_SELECTOR, 'input#startDate')
    date_start_box.send_keys(startYmd)
    sleep(3)

    date_start_box = driver.find_element(By.CSS_SELECTOR, 'input#endDate')
    date_start_box.send_keys(endYmd)
    sleep(3)

# 釣れた日を選択
def select_chokaYmd(driver):
    driver.find_element(By.CSS_SELECTOR,'div.breadcrumb-wrapper div.col-12:nth-of-type(2) > span:nth-of-type(3) > button').click()
    sleep(3)

    driver.find_element(By.CSS_SELECTOR,'div.breadcrumb-wrapper div.col-12:nth-of-type(2) > span:nth-of-type(3) > ul > li:nth-of-type(2)').click()
    sleep(3)

# 最下部にスクロール
def scroll_bottom(driver):
    while True:
        before_height = driver.execute_script("return document.body.scrollHeight")

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(3) 

        after_height = driver.execute_script("return document.body.scrollHeight")

        print('before_height:',before_height,' after_height:',after_height)

        if(before_height == after_height):
            break

# リンク取得
def get_link(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    a_tags = soup.select('div.mb-60 > div:last-of-type div.results > a')

    result = []
    for a_tag in a_tags:
        result.append('https://anglers.jp' + a_tag.get('href'))

    return result

# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # ヘッドレスで起動
# options.add_argument('--no-sandbox') # 仮想環境下では、sandboxで起動すると失敗するので無効にする
# options.add_argument('--disable-gpu') # ヘッドレスモードで起動するときに必要
# options.add_argument('--window-size=1280,1024')  # 画面サイズの指定

# driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(10)

# driver.get('https://anglers.jp/prefectures/3/catches')
# sleep(3)

# print('一覧表示開始')

# input_start(driver, '2022/08/05')
# # select_chokaYmd(driver)
# # scroll_bottom(driver)

# print('一覧表示終了')

# # 一覧のリンク保存
# print('リンク保存開始')

# save_link(driver)

# print('リンク保存終了')

# driver.quit()



 
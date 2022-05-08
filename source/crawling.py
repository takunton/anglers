import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver

# 開始日を入力
def input_start(driver, startYmd):
    driver.find_element_by_css_selector('span[style="display: inline-block;"] > button').click()
    sleep(3)

    date_start_box = driver.find_element_by_css_selector('input#startDate')
    date_start_box.send_keys(startYmd)
    sleep(3)

# 釣れた日を選択
def select_chokaYmd(driver):
    driver.find_element_by_css_selector('div.breadcrumb-wrapper div.col-12:nth-of-type(2) > span:nth-of-type(3) > button').click()
    sleep(3)

    driver.find_element_by_css_selector('div.breadcrumb-wrapper div.col-12:nth-of-type(2) > span:nth-of-type(3) > ul > li:nth-of-type(2)').click()
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

# html出力
def output_html(driver):
    soup = BeautifulSoup(driver.page_source, 'lxml') 
    dir_path = os.path.dirname(os.path.abspath(__file__))

    a_tags = soup.select('div.mb-60 > div:last-of-type div.results > a')
    for i, a_tag in enumerate(a_tags):
        url = 'https://anglers.jp' + a_tag.get('href')
        driver.get(url)
        sleep(3)

    # 釣果情報のhtml保存
        f_name = os.path.join(dir_path, 'html', str(i) + '_choka.html')

        with open(f_name, 'w', encoding='utf-8-sig') as f:
            f.write(driver.page_source)

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(
    executable_path = r'C:\Users\eleve\work\Python\udemy\Scraping_Lesson\section08\tools\chromedriver',
    options=options
    )
driver.implicitly_wait(10)

driver.get('https://anglers.jp/prefectures/3/catches')
sleep(3)

print('一覧表示開始')

input_start(driver, '2021/04/01')
select_chokaYmd(driver)
scroll_bottom(driver)

print('一覧表示終了')

# 一覧のhtml取得
print('html出力開始')

output_html(driver)

print('html出力終了')

driver.quit()



 
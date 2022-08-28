from time import sleep
from selenium import webdriver
import sys
import datetime
import anglers_crawling
import anglers_scraping
import AnglersUtil

# コマンドライン引数の検証
args = sys.argv

if(len(args) != 3):
    print('引数に開始日、終了日を入力してください。')
    exit()

for arg in args[1:]:
    AnglersUtil.IsDate(arg)

# 開始日、終了日をdate変換
startDate = datetime.datetime.strptime(args[1], '%Y%m%d').strftime("%Y/%m/%d")
endDate = datetime.datetime.strptime(args[2], '%Y%m%d').strftime("%Y/%m/%d")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # ヘッドレスで起動
options.add_argument('--no-sandbox') # 仮想環境下では、sandboxで起動すると失敗するので無効にする
# options.add_argument('--disable-gpu') # ヘッドレスモードで起動するときに必要
options.add_argument('--window-size=1280,1024')  # 画面サイズの指定

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

driver.get('https://anglers.jp/prefectures/3/catches')
sleep(3)

print('一覧表示開始')
anglers_crawling.set_date(driver, startDate, endDate)
anglers_crawling.select_chokaYmd(driver)
anglers_crawling.scroll_bottom(driver)
print('一覧表示終了')

print('リンク取得開始')
urls = anglers_crawling.get_link(driver)
print('リンク取得終了')

print('スクレイピング開始')
anglers_scraping.save_data(urls, startDate, endDate)
print('スクレイピング終了')

driver.quit()
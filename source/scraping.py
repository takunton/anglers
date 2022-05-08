import datetime
import glob
import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 釣果情報
d_list = []

dir_path = os.path.dirname(os.path.abspath(__file__))
folder_name = os.path.join(dir_path, 'html')

# 過去の当せん番号
for f_name in glob.glob(folder_name + '/*.html'):
    with open(f_name, 'r', encoding='utf-8-sig') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')

        dd_tags = soup.select('div.content-block > dl > dd')
        
        chokaDate = dd_tags[0].text

        gyoshu_tag = dd_tags[1].select_one('a')
        if(gyoshu_tag):
            gyoshu = gyoshu_tag.text
        else:
            gyoshu = ''

        size = dd_tags[2].text
        weight = dd_tags[3].text
        num = dd_tags[4].text
        tdfk = dd_tags[5].select_one('a').text
        chokaYMD_sort = datetime.datetime.strptime(chokaDate, '%Y年%m月%d日 %H:%M'),

        area_tag = dd_tags[6].select_one('a')
        if(area_tag):
            area = area_tag.text
        else:
            area = ''

        d = {
            'chokaDate': chokaDate,
            'gyoshu': gyoshu,
            'size': size,
            'weight': weight,
            'num': num,
            'tdfk': tdfk,
            'area': area,
            'chokaYMD_sort': chokaYMD_sort
        }

        print(d)
        d_list.append(d)

df = pd.DataFrame(d_list)
df = df.sort_values('chokaYMD_sort')
df = df.drop(columns='chokaYMD_sort')
df.to_csv('choka.csv', index=None, encoding='utf-8-sig')

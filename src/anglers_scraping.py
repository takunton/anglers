import datetime
from time import sleep
import pandas as pd
import requests
from bs4 import BeautifulSoup

def save_data(urls, startYMD, endYMD):
    d_list = []
    for i, url in enumerate(urls):
        print('{}：{}'.format(i + 1, url))

        # ページアクセス
        r = requests.get(url, timeout=15)
        r.raise_for_status()

        # データ抽出
        sleep(15)
        soup = BeautifulSoup(r.content, 'lxml')
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
        chokaYMDHM = datetime.datetime.strptime(chokaDate, '%Y年%m月%d日 %H:%M').strftime('%Y%m%d%H%M')

        area_tag = dd_tags[6].select_one('a')
        if(area_tag):
            area = area_tag.text
        else:
            area = ''

        weather_tag = soup.find(text='天気')
        weather_list = weather_tag.find_next().text.split('　') if weather_tag is not None else ''
        temperture = weather_list[1] if len(weather_list) >= 2 else ''
        wind_direction = weather_list[2] if len(weather_list) >= 3 else ''
        wind_speed = weather_list[3] if len(weather_list) >= 4 else ''
        atmospheric_pressure = weather_list[4] if len(weather_list) >= 5 else ''
        choi_tag = soup.find(text='潮位')
        choi = choi_tag.find_next().text if choi_tag is not None else ''
        tide_tag = soup.find(text='潮名')
        tide = tide_tag.find_next().text if tide_tag is not None else ''
        month_age_tag = soup.find(text='月齢')
        month_age = month_age_tag.find_next().text if month_age_tag is not None else ''
        suii_tag = soup.find(text='水位')
        suii = suii_tag.find_next().text if suii_tag is not None else ''
        previous_rain_tag = soup.find(text='前日雨量')
        previous_rain = previous_rain_tag.find_next().text if previous_rain_tag is not None else ''
        water_discharge_tag = soup.find(text='放水量')
        water_discharge = water_discharge_tag.find_next().text if water_discharge_tag is not None else ''
        water_temperture_tag = soup.find(text='水温')
        water_temperture = water_temperture_tag.find_next().text if water_temperture_tag is not None else ''
        water_depth_tag = soup.find(text='水深')
        water_depth =  water_depth_tag.find_next().text if water_depth_tag is not None else ''
        water_range_tag = soup.find(text='タナ(レンジ)')
        water_range = water_range_tag.find_next().text if water_range_tag is not None else ''

        d = {
            'chokaDate': chokaDate,
            'chokaYMDHM': chokaYMDHM,
            'gyoshu': gyoshu,
            'size': size,
            'weight': weight,
            'num': num,
            'tdfk': tdfk,
            'area': area,
            'temperture': temperture,
            'wind_direction': wind_direction,
            'wind_speed': wind_speed,
            'atmospheric_pressure': atmospheric_pressure,
            'choi': choi,
            'tide': tide,
            'month_age': month_age,
            'suii': suii,
            'previous_rain': previous_rain,
            'water_discharge': water_discharge,
            'water_temperture': water_temperture,
            'water_depth': water_depth,
            'water_range': water_range
        }

        print(d, '\n')
        d_list.append(d)

    df = pd.DataFrame(d_list)
    df = df.sort_values('chokaYMDHM')
    df.to_csv(f'//app/data/choka_{startYMD}_{endYMD}.csv', index=None, encoding='utf-8-sig')

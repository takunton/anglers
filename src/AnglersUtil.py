import datetime

def IsDate(dateStr):
    try:
        date = datetime.datetime.strptime(dateStr, '%Y%m%d')
    except ValueError:
        print('文字列が日付でありません')
        exit()
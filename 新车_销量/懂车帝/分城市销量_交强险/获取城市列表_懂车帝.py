import requests
from datetime import date
import time
import urllib
import pandas as pd
pd.set_option('display.max_columns', None)


## 1、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')


## 2、获取城市列表
def city_list(out_file):
    url = "https://www.dongchedi.com/motor/dealer/m/v1/get_dealer_city_list/"

    headers = {'content-Encoding': "br", 'content-Type': 'application/json'}
    r = requests.get(headers=headers, url=url)
    r_dic = r.json()
    data = r_dic['data']
    for part in data:
        part_data = part['city']
        for city in part_data:
            city_name = city['city_name']
            initials = city['initials']
            results = [initials,city_name]
            write_csv(results,out_file)

out_file = "懂车帝城市列表.csv"
names = ['首字母', '城市名称']
write_csv(names, out_file)  # 写入列名
city_list(out_file)

print("finish!")

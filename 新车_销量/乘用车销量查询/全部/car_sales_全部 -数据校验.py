import requests
from datetime import date
import time
import urllib
import pandas as pd
import json
pd.set_option('display.max_columns', None)
today = date.today()
d1 = today.strftime("%Y%m%d")

## 1、读取品牌列表
def get_brand_dict(brand_file):
    results_dict = {}
    info1 = pd.read_json(brand_file)
    data = info1['data']
    for i in range(0,len(data)):
        info2 = data[i]
        name = info2['name']
        brands = info2['list']
        brand_list = []
        for j in range(0,len(brands)):
            brand = brands[j]['car_name']
            brand_list.append(brand)
        results_dict[name] = brand_list
    return results_dict


## 2、获取车型列表
def get_series_list(brand):
    print(brand)
    series = []
    url = "https://wxapp.autoseles.com/Api/index/car_type?brands={0}&carnev=1".format(urllib.parse.quote(brand))
    headers = {'Content-Encoding': "gzip", 'Content-Type': 'text/html; charset=utf-8'}
    r = requests.get(headers=headers, url=url)
    r_dic = r.json()
    child = r_dic['data'][0]['child'][0]['child']
    for i in range(0,len(child)):
        info = child[i]
        car_name = info['car_name']
        #print(car_name)
        series.append(car_name)
    return series

## 3、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 4、获取内容
def get_content(name,brand,series,output_file):
    base_url = "https://wxapp.autoseles.com/Api/index/contrastList?"
    p1 = "token=f5d4893fa0fe43f79e79e5862ef5a87c&"
    p2 = "pages=1&pages_size=20&brand_1={0}&".format(urllib.parse.quote(brand))
    p3 = "brand_2=&type_1={0}&type_2=&".format(urllib.parse.quote(series))
    p4 = "start_time=2017-1&end_time=2022-9&sales_province=%E5%85%A8%E5%9B%BD&carnev=1"
    url = base_url+p1+p2+p3+p4
    print(url)

    headers = { 'Content-Encoding': "gzip",'Content-Type':'text/html; charset=utf-8'}
    r = requests.get(url=url,headers=headers)
    time.sleep(2)
    r_dic = r.json()
    salesArray1 = r_dic['salesArray1']
    results = [name,brand,series,salesArray1]
    write_csv(results + [d1], output_file)
    print(results)
    r.close()


## 4、写入表头
def write_header_csv(names,out_file):
    write_csv(names, out_file)   #写入列名

brand_file = "品牌列表_全部.json"
city_file = "城市列表.json"
brand_dict = get_brand_dict(brand_file)

name_finished = []
brand_finished = []
series_finished = []
city_finished = []



out_file = "乘用车销量查询_交强险_全国.csv"
log_file = "乘用车销量查询_日志_全国.txt"
names1 = ['字母','品牌','车系','销量','dt']
write_header_csv(names1,out_file)

for name,brand_list in brand_dict.items():
    for brand in brand_list:
        if brand in brand_finished:
            pass
        else:
            log1 = ["开始抓取品牌："+ brand +"   时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())]
            write_csv(log1, log_file)
            series_list = get_series_list(brand)
            for series in series_list:
                if series in series_finished:
                    pass
                else:
                    log2 = ["   开始抓取品牌：" + brand + "  车系  "+series+ "   时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]
                    write_csv(log2, log_file)
                    sales_data = get_content(name,brand, series, out_file)
                    series_finished.append(series)
            print("品牌:  ",brand,"  抓取完毕！")
            brand_finished.append(brand)
print("finish!")



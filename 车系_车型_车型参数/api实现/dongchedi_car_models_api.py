import requests
from datetime import date
import time
import urllib
import pandas as pd
pd.set_option('display.max_columns', None)
today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y/%m/%d")

## 1、读取series_id列表
def get_series_list(input_file):
    df_series = pd.read_csv(input_file)
    series_list = list(df_series['车系ID'])
    return series_list

## 2、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 3、获取内容
def get_content(series_id):
    url = "https://www.dongchedi.com/motor/pc/car/series/car_list?series_id={0}&".format(series_id)
    models_list  = []
    headers = { 'content-type': 'application/json; charset=utf-8',
        'accept-encoding': 'gzip, deflate, br'}
    r = requests.get(headers=headers, url=url)
    r_dic = r.json()
    data1 = r_dic['data']['tab_list']
    for i in range(0,len(data1)):
        data2 = data1[i]
        tab_text = data2['tab_text']  ## 在售，停售
        data_sub = data2['data']
        for j in range(0,len(data_sub)):
            model = data_sub[j]['info']
            #print(tab_text,model)
            if 'id' in model.keys():
                car_name = model['car_name']  ## 车型
                car_id = model['car_id']  ## 车型id
                brand_name = model['brand_name']  ##品牌名称
                brand_id = model['brand_id']  ##品牌id
                series_name = model['series_name']  ## 车系名称
                year = model['year']  ## 年款

                price = model['price'] ##经销商报价
                owner_price = model['owner_price']  ## 车主参考价
                official_price_str = model['official_price_str']  ##指导价
                results = [brand_name, brand_id,tab_text,series_name,series_id,year,car_name, car_id,price,owner_price,official_price_str]
                models_list.append(results)
                print(results)
            else:
                pass
    return models_list

## 4、写入表头
def write_header_csv(out_file):
    names = ['品牌名称','品牌ID','状态','车系名称','车系ID','年款','车型','车型ID','经销商报价','车主参考价','指导价','dt']
    write_csv(names, out_file)   #写入列名

series_file = "D:\\雷神\\pycharm\\新能源爬虫\\车系_车型_车型参数\\车系库_懂车帝_{0}.csv".format(d1)
out_file = "D:\\雷神\\pycharm\\新能源爬虫\\车系_车型_车型参数\\车型库_懂车帝_{0}.csv".format(d1)
write_header_csv(out_file)
series_list = get_series_list(series_file)
for series in series_list:
    models = get_content(series)
    for model in models:
        write_csv(model, out_file)

print("finish!")


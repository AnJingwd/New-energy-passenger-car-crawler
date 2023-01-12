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

## 3、解码价格
def replace_code(str_code):
    # '\ue409.\ue423\ue428-\ue3fd.\ue423\ue428万'  3.28-7.28万
    price_map = {'\ue420': '0', '\ue40d': '1', '\ue423': '2', '\ue409': '3', '\ue41d': '4', '\ue427': '5', '\ue419': '6',
                '\ue3fd': '7', '\ue428': '8', '\ue413': '9'
                }
    str_code_new = str_code.strip()  #去掉首尾空格
    for code,value in price_map.items():
        if code in str_code_new:
            str_code_new = str_code_new.replace(code,price_map[code])
    return str_code_new



## 4、获取内容
def get_series_content(out_file):
    url = "https://www.dongchedi.com/motor/pc/car/brand/select_series_v2"
    series_list  = []
    type = {'4':'纯电','5':'增程','6':'插电式混合动力'}
    for code,type in type.items():
        for page in range(1,200):
            payload = {
                'fuel_form': code,
                'sort_new':'hot_desc',
                'city_name':'北京',
                'limit':'30',
                'page':'{0}'.format(page)
            }
            headers = {}
            r = requests.request("POST", url, headers=headers, data=payload)
            r_dic = r.json()
            data = r_dic['data']['series']
            if len(data) == 0:
                break
            else:
                for i in range(0,len(data)):
                    part = data[i]
                    brand_name = part['brand_name']
                    brand_id = part['brand_id']
                    series_name = part['outter_name']
                    series_id= part['id']

                    dealer_price = replace_code(part['dealer_price'])   ##批发价
                    pre_price = part['pre_price']  ## 报价
                    official_price = part['official_price']  ##官方指导价
                    has_subsidy_price = part['has_subsidy_price'] ## 是否享受补贴
                    subsidy_price = part['subsidy_price'] ##补贴价
                    dcar_score = part['dcar_score'] ## 懂车分
                    if part['top_tag'] :
                        text = part['top_tag']['text']
                    else:
                        text = ''
                    cover_url = part['cover_url']    ##车辆照片
                    results = [brand_name,brand_id,type,series_name,series_id,text,dealer_price,pre_price,official_price,has_subsidy_price,subsidy_price,dcar_score,cover_url]
                    write_csv(results, out_file)
                    print(page,results)

## 4、写入表头
def write_header_csv(out_file):
    names = ['品牌名称','品牌ID','能源类型','车系名称','车系ID','标签','批发价','报价','官方指导价','是否享受补贴','补贴价','懂车分','车辆照片','dt']
    write_csv(names, out_file)   #写入列名



out_file = "D:\\雷神\\pycharm\\新能源爬虫\\车系_车型_车型参数\\车系库_懂车帝_{0}.csv".format(d1)
write_header_csv(out_file)
get_series_content(out_file)

print("finish!")




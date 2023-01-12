import requests
from datetime import date
import time
import urllib
import pandas as pd
pd.set_option('display.max_columns', None)
today = date.today()
d1 = today.strftime("%Y%m%d")

## 1、读取品牌列表
def get_brand_list(brand_file):
    results = []
    info1 = pd.read_json(brand_file)
    data = info1['data']
    for i in range(0,len(data)):
        info2 = data[i]
        brands = info2['list']
        for j in range(0,len(brands)):
            brand = brands[j]['car_name']
            results.append(brand)
            #print(brand)
    return results

## 2、读取城市列表
def get_city_list(city_file):
    results = []
    info1 = pd.read_json(city_file)
    data = info1['data']
    for i in range(0,len(data)):
        info2 = data[i]
        province = info2['city_name']
        info3 = info2['child']
        for j in range(0,len(info3)):
            info4 = info3[j]
            city_name= info4['city_name']
            #print(province,city_name)
            results.append(city_name)
    return results


## 3、获取车型列表
def get_series_list(brand):
    series = []
    url = "https://wxapp.autoseles.com/Api/index/car_type?brands={0}&carnev=2".format(urllib.parse.quote(brand))
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

## 4、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 5、获取内容
def get_content(brand,series,city,output_file):
    #sales_list  = []
    year_month = [("2022-10", "2022-10")]
    #year_month = [("2019-1","2019-12"),("2020-1","2020-12"),("2021-1","2021-12"),("2022-1","2022-9")]
    for y_m in year_month:
        start,end = y_m[0],y_m[1]
        base_url = "https://wxapp.autoseles.com/Api/index/car_list?"
        p1 = "pages=2&pages_size=60&brands={0}&".format(urllib.parse.quote(brand))
        p2 = "sales_province={0}&".format(urllib.parse.quote(city))
        p3 = "start_time={0}&end_time={1}&".format(start,end)
        p4 = "car_type={0}&".format(urllib.parse.quote(series))
        p5 = "token=d5385095a7a0c3edf704830b6daf7bcf&carnev=2"
        url = base_url+p1+p2+p3+p4+p5
        print(url)

        headers = { 'Content-Encoding': "gzip",'Content-Type':'text/html; charset=utf-8'}
        r = requests.get(headers=headers, url=url)
        r_dic = r.json()
        data = r_dic['data']
        for i in range(0,len(data)):
            data_new = data[i]
            sales_province = data_new['sales_province']
            sales_city = data_new['sales_city']
            sales_pinpai = data_new['sales_pinpai']
            sales_car = data_new['sales_car']
            sales_num = data_new['sales_num']
            sales_car_type = data_new['sales_car_type']
            sales_year = data_new['sales_year']
            sales_month = data_new['sales_month']
            results = [sales_year,sales_month,sales_province,sales_city,sales_pinpai,sales_car,sales_num,sales_car_type]
            if sales_num>0:
                write_csv(results + [d1], out_file)
                #sales_list.append(results)
                print(results)
        r.close()
        #time.sleep(1)
    #return sales_list

## 4、写入表头
def write_header_csv(names,out_file):
    write_csv(names, out_file)   #写入列名

brand_file = "品牌列表.json"
city_file = "城市列表.json"
brand_list = get_brand_list(brand_file)
city_list1 = get_city_list(city_file)
city_list = list(filter(None, city_list1))   ##排除None


brand_finished = brand_list[0:92]
series_finished = series_list[0:0]
city_finished = []



out_file = "乘用车销量查询_交强险10月.csv"
log_file = "乘用车销量查询_日志10月.txt"
names1 = ['年份','月份','省份','城市','品牌','车系','销量','类型','dt']
write_header_csv(names1,out_file)

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
                for city in city_list:
                    if city in city_finished:
                        pass
                    else:
                        sales_data = get_content(brand,series,city,out_file)
                        city_finished.append(city)
                        log3 = ['       品牌：'+brand+ "  车系:  "+series+"  "+ "  城市:  "+city+"  抓取完毕   时间："+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())]
                        write_csv(log3, log_file)
                city_finished = []
                series_finished.append(series)
        print("品牌:  ",brand,"  抓取完毕！")
        brand_finished.append(brand)
print("finish!")



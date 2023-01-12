import requests
import pandas as pd
pd.set_option('display.max_columns', None)
from fake_useragent import UserAgent
ua=UserAgent()

from datetime import datetime,date
from dateutil.relativedelta import relativedelta
month_date = datetime.now().date() - relativedelta(months=1)
last_month = month_date.strftime("%m")

today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y%m%d")


## 1、请求网页
def get_html(url):
    headers = {"User-Agent": ua.random, 'Content-type': "application/json;charset=UTF-8"}
    r = requests.get(headers=headers, url=url)
    html_body = r.json()
    r.close()  # 注意关闭response
    return html_body

## 2、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 3、解析网页
def get_city_sales(file):
    base_url = 'https://price.auto.sina.com.cn/api/PaihangbangSales/getSubSalesByParams?'
    para_url = "size=20&page={0}&year={1}&month={2}&carGuidePrice=&serialJiBie=&corpType=&ranliaoXingshi=&serial_id=&need_detail=1"
    for year in range(2020,2023):
        for month in range(1,13):
            for page in range(1,43):
                url = base_url + para_url.format(page,year,month)
                html_body = get_html(url)
                data = html_body['data']['list']
                for i in range(0,len(data)):
                    data_info = data[i]['serial_info']
                    sub_brand_id = data[i]['sub_brand_id']
                    serialZhName = data_info['serialZhName']  # 车系
                    serialLevelName = data_info['serialLevelName']  ## 级别
                    serialAutoTypeName = data_info['serialAutoTypeName']  ## 类型
                    serialGuidePriceRange = data_info['serialGuidePriceRange']  ## 售价
                    brandId = data_info['brandId']  ## 品牌id
                    corpId = data_info['corpId']  ## 厂商id
                    serialId =  data_info['serialId']  ## 车系id
                    sales_volume = data[i]['sales_volume']
                    results = [year,month,brandId,corpId,sub_brand_id,serialId,serialZhName,serialLevelName,serialAutoTypeName,sales_volume,serialGuidePriceRange,page,d2]
                    write_csv(results, file)
            print('第',year,' 年 ',month,' 月 数据','抓取完成!')

out_file = "新浪汽车_车系_月度销量_{0}（交强险）.csv".format(d1)
names = ['年','月份','品牌id','厂商id','子品牌id','车系id','车系名称','级别','类型','销量','指导价','页码','dt']
write_csv(names, out_file)   #写入列名

get_city_sales(out_file)
print('finish!')


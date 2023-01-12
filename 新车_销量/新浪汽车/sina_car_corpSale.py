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
    base_url = 'https://price.auto.sina.cn/api/PaihangbangSales/getCorpSales?'
    para_url = "size=20&page={0}&year={1}&month={2}&need_detail=1"
    for year in range(2020,2023):
        for month in range(1,13):
            for page in range(1,10):
                url = base_url + para_url.format(page,year,month)
                html_body = get_html(url)
                data = html_body['data']['list']
                for i in range(0,len(data)):
                    data_info = data[i]
                    corp_id = data_info['corp_id']  ##厂商id
                    corpName = data_info['corpName']  ## 厂商名称

                    sub_data_info = data_info['big_sales_volume_sub']
                    brand_id = sub_data_info['brand_id']  ## 品牌id
                    sub_brand_id = sub_data_info['sub_brand_id']  ## 子品牌id
                    sub_brand_name = sub_data_info['sub_brand_name']  ## 子品牌名称
                    sales_volume = sub_data_info['sales_volume']
                    results = [year,month,corp_id,corpName,brand_id,sub_brand_id,sub_brand_name,sales_volume,page,d2]
                    write_csv(results, file)
            print('第',year,' 年 ',month,' 月 数据','抓取完成!')

out_file = "新浪汽车_厂商_月度销量_{0}（交强险）.csv".format(d1)
names = ['年','月份','厂商id','厂商名称','品牌id','子品牌id','子品牌名称','销量','页码','dt']
write_csv(names, out_file)   #写入列名

get_city_sales(out_file)
print('finish!')


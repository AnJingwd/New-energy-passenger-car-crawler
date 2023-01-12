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
    base_url = 'https://price.auto.sina.com.cn/api/PaihangbangSales/getBlocSales?'
    para_url = "size=20&page={0}&year={1}&month={2}&need_detail=1"
    for year in range(2020,2023):
        for month in range(1,14):
            for page in range(1,4):
                url = base_url + para_url.format(page,year,month)
                html_body = get_html(url)
                data = html_body['data']['list']
                for i in range(0,len(data)):
                    data_info = data[i]
                    gid = data_info['gid']  ##集团id
                    name = data_info['name']  ## 集团名称
                    sales_volume = data_info['sales_volume']
                    results = [year,month,gid,name,sales_volume,page,d2]
                    write_csv(results, file)
            print('第',year,' 年 ',month,' 月 数据','抓取完成!')

out_file = "新浪汽车_集团_月度销量_{0}（交强险）.csv".format(d1)
names = ['年','月份','集团id','集团名称','销量','页码','dt']
write_csv(names, out_file)   #写入列名

get_city_sales(out_file)
print('finish!')


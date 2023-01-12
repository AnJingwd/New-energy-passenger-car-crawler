import requests,time
import pandas as pd
pd.set_option('display.max_columns', None)
from fake_useragent import UserAgent
ua = UserAgent()

##https://mp.weixin.qq.com/s/DmGPZPqSQ8bxt8b6XXer4A
## 每月13号更新

## 1、请求网页
def get_html(url):
    headers = {"User-Agent": ua.random, 'Content-type': "application/json;charset=UTF-8"}
    r = requests.get(headers=headers, url=url)
    html_body = r.json()
    r.close()  # 注意关闭response
    return html_body

## 2、解析网页
def get_month_sales(year_month,type):
    ## rank_data_type ：排行榜的分类，实测榜:5/城市榜:64/热门榜:1/零售量:11/批发量: 2
    ## new_energy_type=1 纯电动；new_energy_type=2插电混动
    url = "https://www.dongchedi.com/motor/pc/car/rank_data?&month={0}&count=1000&rank_data_type={1}".format(year_month,type)
    html_body = get_html(url)
    num = len(html_body['data']['list'])
    results_list = []
    for i in range(0,num):
        series_id = html_body['data']['list'][i]['series_id']
        series_name = html_body['data']['list'][i]['series_name']
        min_price = html_body['data']['list'][i]['min_price']
        max_price = html_body['data']['list'][i]['max_price']
        rank = html_body['data']['list'][i]['rank']
        count = html_body['data']['list'][i]['count']
        car_review_count = html_body['data']['list'][i]['car_review_count']
        descender_price = html_body['data']['list'][i]['descender_price']
        brand_name = html_body['data']['list'][i]['brand_name']
        sub_brand_name = html_body['data']['list'][i]['sub_brand_name']
        price = html_body['data']['list'][i]['price']
        dealer_price = html_body['data']['list'][i]['dealer_price']
        sale_type = '零售量' if type =='11' else '批发量'
        results = ['2022',month,sale_type,series_id,series_name,min_price,max_price,rank,count,car_review_count,descender_price,
               brand_name,sub_brand_name,price,dealer_price]
        results_list.append(results)
    return results_list


## 3、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

out_file = "懂车帝_21年11月-22年11月零售和批发量（乘联会）.csv"
type_list = ['11','2']  ## 11零售量;  2批发量
month_list = ['202111','202112','202201','202202','202203','202204','202205','202206','202207','202208','202209','202210','202211']
months_finish = []
results = []

for type in type_list:
    for month in month_list:
        month_sales_list = get_month_sales(month,type)
        results.append(month_sales_list)
        months_finish.append(month)
        print('第',month,'月数据爬取完成！')


month_band_price_sales = results
names = ['年','月份','类型','车系id','车系名称','最低价','最高价','排名','本地销量','评论数','降价',
               '品牌名称','子品牌名称','价格区间','经销商价格']
write_csv(names, out_file)   #写入列名

for city_lines in month_band_price_sales:
    for line in city_lines:
        write_csv(line, out_file)

print("finish!")
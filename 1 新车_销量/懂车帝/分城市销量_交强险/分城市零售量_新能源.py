import requests
import pandas as pd
pd.set_option('display.max_columns', None)
from fake_useragent import UserAgent
ua = UserAgent()

from datetime import datetime
from dateutil.relativedelta import relativedelta
month_date = datetime.now().date() - relativedelta(months=1)
last_month = 11 #month_date.strftime("%m")

##https://mp.weixin.qq.com/s/DmGPZPqSQ8bxt8b6XXer4A
#每月18号更新

## 1、请求网页
def get_html(url):
    headers = {"User-Agent": ua.random, 'Content-type': "application/json;charset=UTF-8"}
    r = requests.get(headers=headers, url=url)
    html_body = r.json()
    r.close()  # 注意关闭response
    return html_body

## 2、解析网页
def get_city_sales(city_name,type):
    # {"prompts":"","status":0,"message":"success","data":{"brand_id":{"key":"brand_id","text":"品牌"},"capacity_l":{"data":{"options":[{"param":"0,-1","text":"不限排量"},{"param":"0,1","text":"1.0L及以下"},{"param":"1.1,1.6","text":"1.1-1.6L"},{"param":"1.7,2","text":"1.7-2.0L"},{"param":"2.1,2.5","text":"2.1-2.5L"},{"param":"2.6,3","text":"2.6-3.0L"},{"param":"3.1,4","text":"3.1-4.0L"},{"param":"4,-1","text":"4.0L以上"}]},"icon":"","key":"capacity_l","text":"排量"},"city":{"key":"city","text":"城市"},"filters":[{"icon":"","key":"all","selected_icon":"","text":"全部"},{"data":{"options":[{"param":"0,1,2,3,4,5","text":"全部轿车"},{"param":"0","text":"微型车"},{"param":"1","text":"小型车"},{"param":"2","text":"紧凑型车"},{"param":"3","text":"中型车"},{"param":"4","text":"中大型车"},{"param":"5","text":"大型车"}]},"icon":"https://p3.dcarimg.com/origin/motor-img/52c5bbd6d29978da8a38d7681bea4c73","key":"outter_detail_type","selected_icon":"https://p3.dcarimg.com/origin/motor-img/dae46643d529d124f90916f15d2ad4c2","text":"轿车"},{"data":{"options":[{"param":"10,11,12,13,14","text":"全部SUV"},{"param":"10","text":"小型SUV"},{"param":"11","text":"紧凑型SUV"},{"param":"12","text":"中型SUV"},{"param":"13","text":"中大型SUV"},{"param":"14","text":"大型SUV"}]},"icon":"https://p3.dcarimg.com/origin/motor-img/6a7d45802a5b14ab10ae6592ed938899","key":"outter_detail_type","selected_icon":"https://p3.dcarimg.com/origin/motor-img/278a26e8705440cd7b48ed901da1e49f","text":"SUV"},{"data":{"options":[{"param":"20,21,22,23","text":"全部MPV"},{"param":"20","text":"小型MPV"},{"param":"21","text":"紧凑型MPV"},{"param":"22","text":"中型MPV"},{"param":"23","text":"大型MPV"}]},"icon":"https://p3.dcarimg.com/origin/motor-img/88f2a9135e339de0d3afe43855a1713d","key":"outter_detail_type","selected_icon":"https://p3.dcarimg.com/origin/motor-img/b52d72a852d3c1b7fbceafbd79a2b751","text":"MPV"},{"data":{"options":[{"param":"1,2,3","text":"全部新能源"},{"param":"1","text":"纯电动"},{"param":"2","text":"插电式混动"},{"param":"3","text":"增程式"}]},"icon":"https://p3.dcarimg.com/obj/motor-img/b1fa1122a138ca45d61f4a7a0fe24ead","key":"new_energy_type","selected_icon":"https://p3.dcarimg.com/obj/motor-img/a5393181c9116d7cc5c7af0f69d600e6","text":"新能源"}],"is_publish_time":false,"manufacturer":{"data":{"options":[{"param":"","text":"不限"},{"param":"合资","text":"合资"},{"param":"自主","text":"自主"}]},"key":"manufacturer","text":"厂商"},"new_energy_type":{"data":{"options":[{"param":"1","text":"纯电动"},{"param":"2","text":"插电式混动"}]},"key":"new_energy_type","text":""},"new_version":2,"price":{"data":{"options":[{"param":"0,-1","text":"不限价格"},{"param":"0,5","text":"5万以下"},{"param":"5,8","text":"5-8万"},{"param":"8,12","text":"8-12万"},{"param":"12,18","text":"12-18万"},{"param":"18,25","text":"18-25万"},{"param":"25,35","text":"25-35万"},{"param":"35,-1","text":"35万以上"}]},"icon":"","key":"price","text":"价格"},"score_type":{"data":{"options":[{"param":"score","text":"总榜"},{"param":"comfort","text":"舒适榜"},{"param":"appearance","text":"外观榜"},{"param":"configuration","text":"配置榜"},{"param":"control","text":"操控榜"},{"param":"power","text":"动力榜"},{"param":"space","text":"空间榜"},{"param":"interiors","text":"内饰榜"}]},"icon":"","key":"score_type","text":"懂车分榜单"},"sells_rank_month":[{"text":"2022年09月","month":202209},{"text":"2022年08月","month":202208},{"text":"2022年07月","month":202207},{"text":"2022年06月","month":202206},{"text":"2022年05月","month":202205},{"text":"2022年04月","month":202204},{"text":"近半年","month":500},{"text":"近一年","month":1000}],"tab_list":[{"min_version_code":0,"rank_data_type":20000,"sub_tab_list":[{"min_version_code":0,"rank_data_type":11,"title":"零售量"},{"min_version_code":0,"rank_data_type":2,"title":"批发量"}],"title":"销量榜"},{"min_version_code":0,"rank_data_type":1,"title":"热门榜"},{"min_version_code":600,"rank_data_type":3,"title":"懂车分榜"},{"rank_data_type":10000,"sub_tab_list":[{"min_version_code":0,"rank_data_type":5,"title":"安全榜"},{"min_version_code":0,"rank_data_type":9,"title":"能耗榜"},{"min_version_code":0,"rank_data_type":6,"title":"麋鹿测试"},{"min_version_code":0,"rank_data_type":7,"title":"加速榜"},{"min_version_code":0,"rank_data_type":10,"title":"制动榜"},{"min_version_code":0,"rank_data_type":4,"title":"赛道圈速"}],"title":"实测榜"},{"rank_data_type":10001,"sub_tab_list":[{"min_version_code":0,"rank_data_type":60,"title":"续航榜"},{"min_version_code":0,"rank_data_type":61,"title":"能耗榜"}],"title":"新能源榜"},{"rank_data_type":10002,"sub_tab_list":[{"min_version_code":0,"rank_data_type":64,"title":"热销榜"},{"min_version_code":0,"rank_data_type":52,"title":"降价榜"}],"title":"城市榜"}]}}
    ## rank_data_type ：排行榜的分类，实测榜:5/城市榜:64/热门榜:1/零售量:11/批发量：2
    ##new_energy_type=x 全部新能源；new_energy_type=1 纯电动；new_energy_type=2插电混动;new_energy_type=3增程式; 为空全部乘用车
    type_map = {1:"纯电动",2:"插电混动",3:"增程式"}
    url = "https://www.dongchedi.com/motor/pc/car/rank_data?new_energy_type={0}&month=2022{1}&count=1000&city_name={2}&rank_data_type=64".format(type,last_month,city_name)
    html_body = get_html(url)
    num = html_body['data']['paging']['total']
    if num == 0:
        return -1
    else:
        results_list = []
        for i in range(0,len(html_body['data']['list'])):
            series_id = html_body['data']['list'][i]['series_id']
            series_name = html_body['data']['list'][i]['series_name']
            min_price = html_body['data']['list'][i]['min_price']
            max_price = html_body['data']['list'][i]['max_price']
            rank = html_body['data']['list'][i]['rank']
            count = html_body['data']['list'][i]['count']
            car_review_count = html_body['data']['list'][i]['car_review_count']
            brand_name = html_body['data']['list'][i]['brand_name']
            sub_brand_name = html_body['data']['list'][i]['sub_brand_name']
            price = html_body['data']['list'][i]['price']
            dealer_price = html_body['data']['list'][i]['dealer_price']
            results = [city_name,type_map[type],series_id,series_name,min_price,max_price,rank,count,car_review_count,
                   brand_name,sub_brand_name,price,dealer_price]
            results_list.append(results)
            print(results)
        return results_list

## 3、读取城市列表
def get_city_list(city_file):
    df_city = pd.read_csv(city_file)
    city_list = list(df_city['城市名称'])
    return city_list

## 4、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

city_file = "懂车帝城市列表.csv"
out_file = "懂车帝_22{0}分城市销量_新能源（交强险）.csv".format(last_month)
city_list = get_city_list(city_file)
results = []
citys_finish = []

for type in range(1,4):
    type_map = {1:"纯电动",2:"插电混动",3:"增程式"}
    for city_name in city_list:
        if city_name not in citys_finish:
            city_sales_list = get_city_sales(city_name,type)
            if city_sales_list == -1:
                pass
            else:
                results.append(city_sales_list)
                citys_finish.append(city_name)
                #time.sleep(2)
        else:
            print(type_map[type]," : ",city_name)

city_band_price_sales = results
names = ['城市名','类型','车系id','车系名称','最低价','最高价','排名','本地销量','评论数',
               '品牌名称','子品牌名称','价格区间','经销商价格']
write_csv(names, out_file)   #写入列名
for city_lines in city_band_price_sales:
    for line in city_lines:
        write_csv(line, out_file)

print("finish!")
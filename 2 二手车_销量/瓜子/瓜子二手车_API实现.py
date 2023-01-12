import requests
import pandas as pd
from datetime import date
import urllib
import time,re
pd.set_option('display.max_columns', None)
from fake_useragent import UserAgent
ua=UserAgent()

## https://www.cnblogs.com/gltou/p/16423938.html

main_map = {'&#59854;':'0','&#58397;':'1','&#58928;':'2','&#60146;':'3','&#58149;':'4','&#59537;':'5',
            '&#60492;':'6','&#57808;':'7','&#59246;':'8','&#58670;':'9'
}

## 1、请求网页
def get_html(url):
    headers = {
        'origin': 'https://www.guazi.com',
        'referer': 'https://www.guazi.com/',
        "User-Agent": ua.random,
        "content-type": "text/plain;charset=UTF-8"
    }
    r = requests.get(headers=headers,url=url)
    html_body = r.json()
    r.close()  # 注意关闭response
    return html_body

## 2、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 3、价格解码
def replace_code(str_code,main_map):
    str_code_new = str_code.strip()  #去掉首尾空格
    for code,value in main_map.items():
        if code in str_code_new:
            str_code_new = str_code_new.replace(code,main_map[code])
    return str_code_new

## 4、读取品牌列表
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


def get_location(clueid):
    headers = {
    "authority":"mapi.guazi.com",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cookie": "uuid=657c430b-2adb-4acc-a7e8-6dd77afc262d; cainfo=%7B%22ca_s%22%3A%22seo_google%22%2C%22ca_n%22%3A%22default%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22guid%22%3A%22657c430b-2adb-4acc-a7e8-6dd77afc262d%22%7D; sessionid=a84b97ff-29d9-466b-880b-db563407c079; puuid=08f98de0-4ab8-40e3-d0b1-ac74ea696039; dsnDataObj=%7B%7D; browsingHistoryCount=1",
    "origin": "https://m.guazi.com",
    "referer": "https://m.guazi.com/",
    "sec-ch-ua": 'Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "verify-token": "b9a675e47c10d6641503fa5442f7c27a"
    }
    url = "https://mapi.guazi.com/car-source/carRecord/carInfo?versionId=0.0.0.0&sourceFrom=wap&deviceId=657c430b-2adb-4acc-a7e8-6dd77afc262d&guid=657c430b-2adb-4acc-a7e8-6dd77afc262d&userId=&orgUserId=&unit=&osv=ios&clueId={0}&deviceid=657c430b-2adb-4acc-a7e8-6dd77afc262d&guazi_city=-1&platfromSource=wap".format(clueid)
    r = requests.get(headers=headers,url=url)
    html_body = r.json()
    r.close()  # 注意关闭response
    data = body['data']['postList']
    return location


today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y/%m/%d")

output_file = "瓜子二手车_新能源_{0}.csv".format(d1)
brand_file = "品牌列表_新能源.json"
names = ['品牌','能源类型','车系','车型','标题','价格','上牌地','puid','clue_id','详情页url','page','dt']
write_csv(names, output_file)   #写入列名
brand_list = get_brand_list(brand_file)
brand_finished = []#brand_list[0:115]



## fuel_type=3  纯电； fuel_type=4  油电混动
for type in (3,4):
for brand in brand_list:
    if brand in brand_finished:
        pass
    else:
        for i in range(1,1000):
            time.sleep(5)
            url = "https://mapi.guazi.com/car-source/carList/pcList?" \
                  "versionId=0.0.0.0&sourceFrom=wap&deviceId=657c430b-2adb-4acc-a7e8-6dd77afc262d&osv=Windows+10&minor=&sourceType=&ec_buy_car_list_ab=" \
                  "&location_city=&district_id=&tag=-1&license_date=&auto_type=&driving_type=&gearbox=&road_haul=&air_displacement=&emission=&" \
                  "car_color=&guobie=&bright_spot_config=&seat=&fuel_type={0}&order=&priceRange=0,-1&tag_types=&diff_city=&" \
                  "intention_options=&initialPriceRange=&monthlyPriceRange=&transfer_num=&car_year=&" \
                  "carid_qigangshu=&carid_jinqixingshi=&cheliangjibie=&key_word={1}&" \
                  "page={2}&pageSize=20&city_filter=12&city=12&guazi_city=12&qpres=&platfromSource=wap".format(type,urllib.parse.quote(brand),i)
            print(url)
            body = get_html(url)
            data = body['data']['postList']
            if len(data) == 0:
                break
            else:
                for j in range(0,len(data)):
                    page = i
                    title = data[j]['title']
                    print(title)
                    years = re.findall(u"[0-9]{4}款|[0-9]{4}", title)[0]
                    series,model = title.split(years)[0],title.split(years)[1]
                    price = replace_code(data[j]['price'],main_map)
                    clue_id = data[j]['clue_id']
                    puid = data[j]['puid']
                    detail_url = 'https://www.guazi.com/Detail?clueId='+str(clue_id)
                    #location = get_location(detail_url)
                    type_name = "纯电" if type ==3 else "插混"
                    results = [brand,type_name,series,model,title,price,puid,clue_id,detail_url,page,d2]
                    print(results)
                    write_csv(results,output_file)

print("finish!")

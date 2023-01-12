import requests
from datetime import date
import pandas as pd
pd.set_option('display.max_columns', None)
from fake_useragent import UserAgent
ua = UserAgent()
from lxml import etree
import time,re
from collections import defaultdict


## 1、请求网页
def get_html(url):
    headers = {
        "User-Agent": ua.random,
        "content-type": "text/plain;charset=UTF-8"
    }
    r = requests.get(headers=headers,url=url)
    html_body = r.text
    r.close()  # 注意关闭response
    return html_body

#\uE49D\uE534\u002E\uE45D\uE4E3\uE40A   36.98万
#\uE463\uE41D\u002E\uE439\uE54C\uE40A   24.01万
#\uE463\uE525\u0020\u007C\u0020\uE41D\u002E\uE54C\uE54C\uE40A\uE492\uE4A8   2年|4.11万公里
#\uE463\uE525\uE411\uE531\uE434\u0020\u007C\u0020\uE49D\u002E\uE4E3\uE49D\uE40A\uE492\uE4A8   2年5个月|3.83万公里
#\uE54C\uE525\uE463\uE531\uE434\u0020\u007C\u0020\uE439\u002E\uE463\uE41D\uE40A\uE492\uE4A8  1年2个月|0.24万公里

main_map = {'\ue439':'0','\ue54c':'1','\ue463':'2','\ue49d':'3','\ue41d':'4','\ue411':'5','\ue534':'6','\ue3eb':'7','\ue4e3':'8','\ue45d':'9',
            '\002e':'.','\ue40a':'万','\ue525':'年','\ue531':'个','\ue434':'月','\007c':'|','\ue492':'公','\ue4a8':'里','\ue45f':'上','无':'\ue4aa','\ue42d':'报'
}

# ['\ue3f0\ue453\ue3f0\ue3f0\ue485\ue453\ue422\ue415\ue53e牌']  2022年03月上牌
detail_map = {'\ue453':'0','\ue53d':'1','\ue3f0':'2','\ue422':'3','\ue42c':'4','\ue49c':'5','\ue42b':'6','\ue4fe':'7','\ue548':'8','\ue4c8':'9',
            '\ue485':'年','\ue415':'月','\ue53e':'上'
}


def replace_code(str_code,main_map):
    str_code_new = str_code.strip()  #去掉首尾空格
    for code,value in main_map.items():
        if code in str_code_new:
            str_code_new = str_code_new.replace(code,main_map[code])
    return str_code_new


def get_detail_info(detail_url,detail_map):
    detail_body = get_html(detail_url)
    res_detail = etree.HTML(detail_body)
    ## 车况
    try:
        license_time = replace_code(res_detail.xpath('//*[@id="__next"]/div/div[2]/div/div[2]/div[2]/div[5]/div/div[1]/p[2]/text()')[0],detail_map)
    except:
        license_time = ""
    try:
        transfer = res_detail.xpath('/html/body/div[1]/div[1]/div[2]/div/div[4]/div[2]/div[1]/div/div[3]/p[1]/text()')[0]  ## 过户次数
    except:
        transfer = ""
    try:
        car_city = res_detail.xpath('//*[ @ id = "1"]/div[2]/div[1]/div/div[2]/p[1]/text()')[0]  ## 车源地
    except:
        car_city = ""
    try:
        license_city = res_detail.xpath('//*[@id="1"]/div[2]/div[1]/div/div[1]/p[1]/text()')[0]   ## 上牌地
    except:
        license_city = ""
    try:
        car_out_color = res_detail.xpath('//*[@id="1"]/div[2]/div[1]/div/div[8]/p[1]/text()')[0]   ## 车身颜色
    except:
        car_out_color = ""
    try:
        car_in_color = res_detail.xpath('//*[@id="1"]/div[2]/div[1]/div/div[9]/p[1]/text()')[0]   ## 内饰颜色
    except:
        car_in_color = ""
    #car_condition = res_detail.xpath('//*[@id="1"]/div[2]/div[2]/p/text()')[0]

    ## 商家信息
    try:
        owner_name = res_detail.xpath('//*[@id="3"]/div[2]/div[2]/p[1]/text()')[0]
    except:
        owner_name = ""
    try:
        owner_cars = res_detail.xpath('//*[@id="3"]/div[2]/div[2]/div[1]/p[1]/text()')[0]
    except:
        owner_cars = ""
    try:
        owner_region = res_detail.xpath('//*[@id="3"]/div[2]/div[2]/div[1]/p[2]/text()')[0]
    except:
        owner_region = ""
    try:
        owner_adress = res_detail.xpath('//*[@id="3"]/div[2]/div[2]/p[2]/text()[2]')[0]
    except:
        owner_adress = ""
    #owner_call = res_detail.xpath('//*[@id="3"]/div[2]/div[2]/div[2]/p[2]/text()')[0]    ## 点击查看联系电话
    result_part2 = [car_city,license_time,transfer,license_city,car_out_color,car_in_color,
                    owner_name,owner_cars,owner_adress]
    return result_part2


## 4、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')


today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y/%m/%d")
out_file = "懂车帝二手车_全部新能源_{0}.csv".format(d1)
names = ['carid','类型','page','车系','年款','车型','标题','上牌年限','公里数（万公里）','二手车售价','新车售价','详情页url',
         '车源地', '上牌时间','过户次数','上牌地','车身颜色','内饰颜色','车商名称','在售车源数','车商地址','dt']
url_dict = {
  '纯电20w下':["https://www.dongchedi.com/usedcar/0,20-x-x-x-x-x-4-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-1-x-x-x-x-x",
            "https://www.dongchedi.com/usedcar/0,20-x-x-x-x-x-4-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-{0}-x-x-x-x-x"],
  '纯电20w上': ["https://www.dongchedi.com/usedcar/20,!1-x-x-x-x-x-4-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-1-x-x-x-x-x",
             "https://www.dongchedi.com/usedcar/20,!1-x-x-x-x-x-4-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-{0}-x-x-x-x-x"],
  '插混': ["https://www.dongchedi.com/usedcar/x-x-x-x-x-x-6-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-1-x-x-x-x-x",
         "https://www.dongchedi.com/usedcar/x-x-x-x-x-x-6-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-{0}-x-x-x-x-x"],
  '增程': ["https://www.dongchedi.com/usedcar/x-x-x-x-x-x-5-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-1-x-x-x-x-x",
         "https://www.dongchedi.com/usedcar/x-x-x-x-x-x-5-x-x-x-x-x-x-x-x-x-x-x-x-x-x-1-{0}-x-x-x-x-x"]
}
write_csv(names, out_file)   #写入列名

def get_page_nums(url1):
    html_body = get_html(url1)
    res = etree.HTML(html_body)
    try:
        page_num = int(res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/div[4]/ul/li[7]/a/span/text()')[0])
    except:
        page_num = 167  ## 懂车帝二手车，页面限制，最多显示167页
    return page_num


## 1页 15行，每行4个
planed_pages_dict,screen_pages_dict,cars_num_dict = defaultdict(list),defaultdict(list),defaultdict(list)

for type,urls in url_dict.items():
    url1,url2 = urls[0],urls[1]
    page_num = get_page_nums(url1)
    strat_page = 1 if type !="纯电20w下" else 85

    cars_num_dict[type] = 0   ##记录累计爬取车辆数
    for page in range(strat_page,page_num+1):
        planed_pages_dict[type].append(page)
        time.sleep(2)
        url =url2.format(page)
        html_body = get_html(url)
        res = etree.HTML(html_body)
        for i in range(1,61):
            try:
                title = res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/ul/li[{0}]/a/dl/dt/p/text()'.format(i))[0]
            except:
                break
            license_distance = res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/ul/li[{0}]/a/dl/dd[1]/text()'.format(i))[0]  ##上牌时长，公里数
            price_code = res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/ul/li[{0}]/a/dl/dd[3]/text()'.format(i))[0]  ## 二手车价格
            new_price_code = res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/ul/li[{0}]/a/dl/dd[3]/span/text()'.format(i))[0]  ## 新车指导价
            detail_url = res.xpath('//*[@id="__next"]/div[1]/div[2]/div/div/div[2]/ul/li[{0}]/a/@href'.format(i))[0]
            carid = detail_url.split("/")[-1]

            license,distance = replace_code(license_distance.split("|")[0], main_map),replace_code(license_distance.split("|")[1],main_map)
            price,new_price = replace_code(price_code,main_map),replace_code(new_price_code.split(" ")[-1],main_map)
            detail_url_link = "https://www.dongchedi.com"+detail_url
            years = re.findall(u"[0-9]{4}款|[0-9]{4}", title)[0]
            series, model = title.split(years)[0], title.split(years)[1]
            result_part1 = [carid,type,page,series,years,model,title,license,distance,price,new_price,detail_url_link]
            result_part2 = get_detail_info(detail_url_link,detail_map)
            cars_num_dict[type] +=1
            write_csv(result_part1+result_part2+[d2], out_file)
            planed_pages_dict[type].append(page)
            print( " type: ",type,"  page: ",page,"  carid: ",carid,"  本页第{0}辆".format(i),"  累计已爬{0}辆".format(cars_num_dict[type]))

for type,pages in planed_pages_dict.items():
    skep_pages = sorted(list(set(planed_pages_dict[type])-set(screen_pages_dict[type])))
    if len(skep_pages) ==0:
        print(type,"  抓取完成!")
    else:
        print(type, " 遗漏页为：",skep_pages)






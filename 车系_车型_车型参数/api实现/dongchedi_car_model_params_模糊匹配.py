import requests
from datetime import date
import time
import pandas as pd
pd.set_option('display.max_columns', None)
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.page_load_strategy = 'normal'
import operator
today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y/%m/%d")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.relative_locator import with_tag_name

## 1、读取car_id列表
def get_models_list(input_file,series_list):
    df_series = pd.read_csv(input_file)
    df_series_sub = df_series[df_series['车系名称'].isin(series_list)]
    model_list = list(df_series_sub['车型ID'])
    return model_list

## 2、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

##4、获取车型参数列表
title_list0 = []
def get_content(car_id,output_file):
    global title_list0
    url = 'https://www.dongchedi.com/auto/params-carIds-{0}'.format(car_id)
    print(url)
    browser = webdriver.Chrome()
    time.sleep(2)
    browser.refresh()
    browser.get(url)

    today = date.today()
    d1 = today.strftime("%Y/%m/%d")

    title_list,content_list = [],[]
    models = browser.find_element('xpath','//*[@id="__next"]/div/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/h1/a').text   ##标题
    for i in range(1,300):
        try:
            eles = browser.find_element("xpath", "(//div[@data-row-anchor])[{0}]".format(i))
        except:
            break
        atts = eles.get_attribute("data-row-anchor")
        text = browser.find_element("xpath", "//div[@data-row-anchor='{0}']".format(atts)).text
        len_text = len(text.split('\n', 1))
        title = text.split('\n', 1)[0]
        content = text.split('\n',1)[1:] if len_text>1 else "-"
        title_list.append(title)
        content_list.append(content[0])
    print([url,models]+content_list+[d1])
    if not operator.eq(title_list0,title_list):
        write_csv(['详情页url','车型']+title_list+['dt'], output_file)
        write_csv([url,models]+content_list+[d1], output_file)
        title_list0 = title_list
    else:
        write_csv([url,models]+content_list+[d1], output_file)
    browser.close()



input_file = "D:\\雷神\\pycharm\\新能源爬虫\\车系_车型_车型参数\\车型库_懂车帝_{0}.csv".format(d1)
series_list = [
                '宋PLUS EV','秦PLUS EV','唐EV','唐DM','元Pro','海豚',
                '海豹','汉EV','元PLUS',
                '蔚来ES6','蔚来ES8','蔚来EC6','蔚来ET7','蔚来ET5',
                '理想L9','理想L8','理想ONE',
                'ZEEKR 001',
                '小鹏P7',
                'Model 3','Model Y',
                'Model S','Model X','Model Y(海外)',
                'AION Y','AION S',
                '宝马iX3',
                'ID.4 X','ID.4 CROZZ','ID.6 X','ID.6 CROZZ',
                '欧拉好猫','欧拉黑猫','欧拉白猫',
                '五菱宏光MINIEV',
                '高合HiPhi Z','高合HiPhi X','Taycan','岚图FREE'
               ]
car_ids = get_models_list(input_file,series_list)
out_file = "D:\\雷神\\pycharm\\新能源爬虫\\车系_车型_车型参数\\车型参数_懂车帝_{0}.csv".format(d1)
for i in range(0,len(car_ids)):
    #print(car_ids[i])
    get_content(car_ids[i],out_file)

print("finish!")



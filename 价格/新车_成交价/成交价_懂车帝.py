import requests
from datetime import date
import pandas as pd
pd.set_option('display.max_columns', None)

today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y/%m/%d")

## 1、读取models_id列表
def get_models_list(input_file):
    df_models = pd.read_csv(input_file)
    models_list = list(df_models['车型ID'])
    return models_list

## 2、结果追加写入csv
def write_csv(list,file):
    df = pd.DataFrame([list])
    df.to_csv(file, mode= 'a',index=False, header=False,encoding='utf_8_sig')

## 3、获取内容
def get_models_content(model_id,out_file):
    url = "https://www.dongchedi.com/motor/pc/car/series/car_price_list?car_id={0}&city_name=&selected_city_name=%E5%85%A8%E5%9B%BD&page=1&pageSize=100".format(model_id)
    payload = {}
    headers = {}
    r = requests.request("GET", url, headers=headers, data=payload)
    r_dic = r.json()
    data = r_dic['data']['car_price_data_list']
    total = r_dic['data']['total']
    print(url)
    if total == 0:
        pass
    else:
        for i in range(0, len(data)):
            item = data[i]
            bought_city_name = item['bought_city_name']
            bought_time = item['bought_time']
            naked_price = item['naked_price']
            has_naked_price = item['has_naked_price']
            full_price = item['full_price']
            has_full_price = item['has_full_price']
            pay_type = item['pay_type']
            notes = item['notes']
            item_id_str = item['has_naked_price']
            show_invoice = item['show_invoice']
            img_info = item['img_info']
            img_url = item['img_url']
            data_from = item['data_from']
            results = [model_id,bought_city_name, bought_time, naked_price, has_naked_price, full_price, has_full_price, pay_type, notes, item_id_str,
               show_invoice, img_info, img_url, data_from,d2]
            write_csv(results, out_file)
            print(results)

models_file = "车型库_懂车帝1208.csv"
out_file = "新车成交价_懂车帝_{0}.csv".format(d1)
names = ['车型ID','购买城市','购买日期','裸车价','是否有裸车价','总价','是否有总价','支付类型','备注','item_id_str','是否展示发票','图片信息','图片链接','数据来源','dt']
write_csv(names, out_file)   #写入列名
models_list = get_models_list(models_file)
for model_id in models_list:
    get_models_content(model_id,out_file)

print("finish!")



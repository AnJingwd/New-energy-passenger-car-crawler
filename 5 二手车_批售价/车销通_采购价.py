import time
import requests
import pandas as pd
from datetime import date,timedelta
import json
from fake_useragent import UserAgent
ua=UserAgent()

today = date.today()
d1 = today.strftime("%Y%m%d")
d2 = today.strftime("%Y-%m-%d")
date_7_before = today + timedelta(days=-6)
d7 = date_7_before.strftime("%Y-%m-%d")
date_14_before = today + timedelta(days=-900)
d14 = date_14_before.strftime("%Y-%m-%d")


def get_auth():
    ## 获取验证码
    url = "http://cxtapi.easypass.cn/api/user/identity/auth"
    headers = {
        "Host":"cxtapi.easypass.cn",
        "Content-Type":"application/json",
        "Connection":"keep-alive",
        "Accept":"*/*",
        "User-Agent":"CYTEasyPass/4.15.17 (iPhone; iOS 14.7.1; Scale/3.00)",
        "Accept-Language":"zh-Hans-CN;q=1",
        "Content-Length":"177",
        "Accept-Encoding":"gzip, deflate, br"
    }
    payload = {
        "deviceId": "f320f7f30ba84f409d95fab185ce84cc",
        "password":"",
        "mobile":"",
        "userId":"303674",
        "refreshToken":"9fa75eea-33a6-4a16-939c-127d65301b94",
        "grantType":"2",
        "tokenValue":""
    }
    r = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
    r_dic = r.json()
    accessToken = r_dic['data']['accessToken']
    r.close()
    if len(accessToken)>10:
        return "Bearer "+accessToken

## 1、请求网页
def get_html(url):
    headers = {
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

## 3、获取品牌列表
def get_brand_list():
    brand_list = []
    url = "http://cxtapi.easypass.cn/api/car/model/masterbrands?containsPi=true&type=mergecarsource_filter"
    body = get_html(url)
    data = body['data']['list']
    for i in range(0,len(data)):
        groupName = data[i]['groupName']
        masterBrandName = data[i]['masterBrands']
        #print(groupName,masterBrandName)
        for j in range(0,len(masterBrandName)):
            BrandId = masterBrandName[j]['masterBrandId']
            BrandName= masterBrandName[j]['masterBrandName']
            #print(groupName,BrandId,BrandName)
            results = [groupName,BrandId,BrandName]
            brand_list.append(results)
    return brand_list


## 4、获取车型列表
def get_model_list(brandId):
    model_list = []
    url = "http://cxtapi.easypass.cn/api/car/model/makeandmodels?brandId={0}&type=mergecarsource_filter".format(brandId)
    body = get_html(url)
    data = body['data']['list']
    if len(data) == 0:
        return []
    else:
        for i in range(0,len(data)):
            models = data[i]['models']
            for i in range(0,len(models)):
                model = models[i]
                modelId = model['modelId']
                modelName = model['modelName']
                results = [brandId, modelId, modelName]
                model_list.append(results)
        return model_list


## 5、获取carid列表
def get_carid_list(modelId):
    carid_list = []
    url = "http://cxtapi.easypass.cn/api/car/common/getGroupCarInfoListByModelId?serialId={0}&type=mergecarsource_filter".format(modelId)
    body = get_html(url)
    data = body['data']['list']
    for i in range(0,len(data)):
        years = data[i]['groupName']
        cars = data[i]['cars']
        for j in range(0,len(cars)):
            carId = cars[j]["carId"]
            carName = cars[j]["carName"]
            carReferPrice = cars[j]["carReferPrice"]   ##参考价
            count = cars[j]["count"]                   ##车源数
            results = [modelId,years,carId,carName,carReferPrice,count]
            carid_list.append(results)
            #print(results)
    return carid_list

## 6、获取采购价
def get_price_list(carSerialId,carId,output_file,Authorization,phones_file,df_phones):
    url = "http://cxtapi.easypass.cn/api/car/source/getListByConditions"
    ## Authorization会失效，要更新
    headers = {
        "User-Agent": "CYTEasyPass/4.15.17 (iPhone; iOS 14.7.1; Scale/3.00)",
        "devicePlatform": "iPhone12,3",
        "userId": "303674",
        "clientId": "app",
        "appVersion": "4.15.17",
        "latitude": "0.000000",
        "os": "ios",
        "deviceId": "f320f7f30ba84f409d95fab185ce84cc",
        "longitude": "0.000000",
        "Authorization": Authorization,
        "Accept-Language": "zh-Hans-CN;q=1",
        "x-theme": "normal",
        "osVersion": "14.7.1",
        "appBuild": "0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Accept-Encoding":"gzip, deflate, br"
    }
    payload = {
        "keyword": "", "carSerialId": carSerialId, "locationGroupId": -1, "exteriorColor": "", "query": "", "lastId": 0,
         "longitude": 0, "latitude": 0, "source": 2, "carId": carId, "dealerMemberLevelId": -1, "provinceId": -1,
         "sort": -1
    }
    r = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)
    # 打印网页真实编码
    #print(r.apparent_encoding)
    r.encoding = "utf-8"
    #print(r.text)
    r_dic = r.json()
    items = r_dic["data"]["list"]
    for i in range(0,len(items)):
        carSourceInfo = items[i]
        carSourceInfo2= carSourceInfo['carSourceInfo']
        #print(carSourceInfo)
        verifyAuditStatus = carSourceInfo2['verifyAuditStatus']  ## 验证审核状态
        brandName = carSourceInfo2['brandName']  ## 品牌
        serialName = carSourceInfo2['serialName']  ## 车系
        carYearType = carSourceInfo2['carYearType']  ## 车型
        fullCarName = carSourceInfo2['fullCarName'] ## 车名
        carSourceId = carSourceInfo2['carSourceId']
        exteriorColor = carSourceInfo2['exteriorColor']
        interiorColor = carSourceInfo2['interiorColor']
        carSourceAddress = carSourceInfo2['carSourceAddress']  ##车源地
        carReferPrice = carSourceInfo2['carReferPrice']  ## 指导价
        salePrice = carSourceInfo2['salePrice']  ## 报价
        priceMode = carSourceInfo2['priceMode']  ##0 电议；1 降价 2 降百分点 3 加价  4 无
        if priceMode == 0:
            priceMode_name = "电议"
        elif priceMode == 1:
            priceMode_name = "降价"
        elif priceMode == 2:
            priceMode_name = "降百分点"
        elif priceMode == 3:
            priceMode_name = "加价"
        elif priceMode == 4:
            priceMode_name = "未报价"
        else:
            priceMode_name = "未知"
        priceBasicPoint = carSourceInfo2['priceBasicPoint'] ## 调价
        publishTime = carSourceInfo2['publishTime']  ##调价时间
        if ":" in publishTime :   ## 三种时间：  09:33    01-05  2022-12-26
            publishTime = d2+" "+ publishTime
        elif len(publishTime)==5 and "-" in publishTime:
            publishTime = "2023-"+publishTime
        else:
            publishTime
        carSourceInfo3 = carSourceInfo['dealer']
        userName = carSourceInfo3['userName']

        phone = get_phone(carSourceId,Authorization)
        if publishTime>=d14:
            phone_location = get_phone_location(phone,df_phones)
            province,city = phone_location[1],phone_location[2]
            if phone not in list(df_phones['电话号码']):
                write_csv(phone_location, phones_file)
        else:
            province,city = "",""
        results = [userName,phone,province,city,verifyAuditStatus,carSourceId,brandName,serialName,carYearType,fullCarName,exteriorColor,interiorColor,carSourceAddress,carReferPrice,salePrice,priceMode_name,priceBasicPoint,publishTime,d1]
        if len(results) >0:
            print(results)
            write_csv(results, output_file)
    r.close()

def get_phone(carSourceId,Authorization):
    #print("carSourceId: ",carSourceId )
    url = "https://cxtapi.easypass.cn/api/gw/car/source/getTelphone?carSourceId={0}".format(carSourceId)  #4907433
    ## Authorization会失效，要更新
    headers = {
            "Host":"cxtapi.easypass.cn",
            "Accept":"*/*",
            "userId":"303674",
            "longitude":"0.000000",
            "x-theme":"normal",
            "latitude":"0.000000",
            "clientId":"app",
            "devicePlatform":"iPhone12,3",
            "os":"ios",
            "Accept-Language":"zh-Hans-CN;q=1",
            "appVersion":"4.15.17",
            "deviceId":"f320f7f30ba84f409d95fab185ce84cc",
            "User-Agent":"CYTEasyPass/4.15.17 (iPhone; iOS 14.7.1; Scale/3.00)",
            "Accept-Encoding":"gzip, deflate, br",
            "appBuild":"0",
            "Connection":"keep-alive",
            "Authorization":Authorization,
            "osVersion":"14.7.1"
    }
    payload = {

    }
    r = requests.request("GET", url, headers=headers)
    r_dic = r.json()
    try:
        phone = r_dic["data"]["phone"]
    except:
        phone = ""
    r.close()
    return phone

def get_phone_location(phone,df_phones):
    ## 极速数据：https://www.jisuapi.com/debug/shouji/
    phone_list = list(df_phones['电话号码'])
    if phone in phone_list:
        df_phones_sub = df_phones[df_phones["电话号码"] == phone]
        return [df_phones_sub.iloc[0]['电话号码'],df_phones_sub.iloc[0]['归属省份'],df_phones_sub.iloc[0]['归属城市']]
    else:
        url = "https://api.jisuapi.com/shouji/query?appkey=43f0c702fd45548e&shouji={0}".format(phone)
        r = requests.get(url=url)
        html_body = r.json()
        province = html_body['result']['province']
        city = html_body['result']['city']
        return [phone,province,city]

output_file = "车销通二手车_C1批售价_{0}.csv".format(d1)
names = ['车商姓名','车商电话',"归属省份","归属城市",'验证审核状态','carSourceId','品牌','车系','年款','车名','车身颜色','内饰颜色','车源地','新车指导价','报价','调价类型','调价金额/百分点','调价时间','dt']
phones_file= "车销通_车商电话归属地.csv"
df_phones = pd.read_csv(phones_file)
names_phone = ["电话号码","归属省份","归属城市"]
write_csv(names, output_file)   #写入列名
write_csv(names_phone, phones_file)

brand_finished = []
model_finished = [] #model_list[0:33]
carid_finished = []

#brand_list = get_brand_list()
brand_list = [['B', 15, '比亚迪'],['W', 266, '蔚来'], ['L', 309, '理想汽车'],
              ['J', 450, '极氪'],['X', 297, '小鹏汽车'], ['T', 189, '特斯拉'],
              ['A', 295, '埃安'],['B', 3, '宝马'], ['D', 8, '大众'],
              ['O', 305, '欧拉'], ['W', 48, '五菱汽车'], ['B', 82, '保时捷'],
              ['L', 402, '岚图汽车']]
def get_model_list_sub(brand_id):
    if brand_id == 15:
        return [[15, 6157, '汉'],[15, 7350, '宋PLUS新能源'],[15, 7219, '秦PLUS新能源'],[15, 5521, '唐新能源'],[15, 5380, '元新能源'],[15, 7480, '海豚'], [15, 7669, '海豹']]
    elif brand_id == 266:
        return [[266, 6213, '蔚来EC6'], [266, 5551, '蔚来ES6'], [266, 5033, '蔚来ES8']]
    elif brand_id == 309:
        return [[309, 8894, '理想L8'], [309, 8105, '理想L9'], [309, 5486, '理想ONE']]

    elif brand_id == 450:
        return [[450, 7440, 'ZEEKR 001']]
    elif brand_id == 297:
        return [[297, 5694, '小鹏汽车P7']]
    elif brand_id == 189:
        return [[189, 5845, 'Model 3'], [189, 6224, 'Model Y'], [189, 4759, 'Model 3(进口)'], [189, 3843, 'Model S'],[189, 3844, 'Model X'], [189, 5646, 'Model Y(进口)']]

    elif brand_id == 295:
        return [[295, 5536, 'AION S'], [295, 7229, 'AION Y']]
    elif brand_id == 3:
        return [[3, 6731, '宝马iX3']]
    elif brand_id == 8:
        return [ [8, 6208, 'ID.4 X'], [8, 7383, 'ID.6 X'], [8, 6835, 'ID.4 CROZZ'], [8, 7416, 'ID.6 CROZZ']]

    elif brand_id == 305:
        return [[305, 6878, '欧拉好猫'],  [305, 5793, '欧拉白猫'], [305, 5446, '欧拉黑猫']]
    elif brand_id == 48:
        return [[48, 6580, '宏光MINIEV']]
    elif brand_id == 82:
        return [[82, 5407, 'Taycan']]

    elif brand_id == 402:
        return [[402, 7136, '岚图FREE 纯电版']]

num = 0
Authorization = get_auth()
for brand_info in brand_list:
    if num//39 ==0:
        Authorization = get_auth()
    symbol,brand_id,brand_name = brand_info[0],brand_info[1],brand_info[2]
    #print(brand_id,brand_name)
    if brand_info in brand_finished:  ##过滤1
        pass
    else:
        #model_list = get_model_list(brand_id)
        model_list = get_model_list_sub(brand_id)
        print(model_list)
        if len(model_list) == 0:   ## ##过滤2
            pass
        else:
            for model_info in model_list:
                model_id,model_name = model_info[1],model_info[2]
                if model_info in model_finished:  ## ##过滤3
                    pass
                else:
                    carid_list = get_carid_list(model_id)
                    for car_info in carid_list:
                        carid,carname,referprice,count = car_info[2],car_info[3],car_info[4],car_info[5]
                        time.sleep(1)
                        if carid in carid_finished:
                            pass
                        else:
                            results = get_price_list(model_id, carid, output_file,Authorization,phones_file,df_phones)
                            carid_finished.append(carid)
                            num += 1
                            if results:
                                if results[12] == "***":
                                    break
                                else:
                                    write_csv(results, output_file)
                                    print(results)
                    model_finished.append(model_info)
        brand_finished.append(brand_info)
        print(" 品牌 ",brand_name, "  抓取完毕！ " )

print("finish!")

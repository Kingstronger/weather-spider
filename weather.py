# -*- coding:utf-8 -*-
import string
import urllib.request
# import demjson
from bs4 import BeautifulSoup
import re
import  json
import time
import sqlite3
#pxt_edit
# # def save_as_excel(weather_date, weather_position_name, weather_list):
#
#     excelname =  weather_position_name + weather_date
#     time_list = []
#     time_list.append("时间(h)")
#     temperature_list = []
#     temperature_list.append("温度(℃)")
#     rain_list = []
#     rain_list.append("降雨量(mm)")
#     humidity_list = []
#     humidity_list.append("相对湿度(%)")
#     wind_list = []
#     wind_list.append("风力风向")
#     for item in weather_list:
#         time_list.append(item['od21'])
#         temperature_list.append(item['od22'])
#         rain_list.append(item['od26'])
#         humidity_list.append(item['od27'])
#         wind_list.append(item['od24']+item['od25'])
#         # print item
#
#     wb = openpyxl.Workbook()
#     wb.create_sheet(index=0,title=weather_date);
#     sheet = wb.get_sheet_by_name(weather_date)
#
#     sheet.append(time_list)
#     sheet.append(temperature_list)
#     sheet.append(rain_list)
#     sheet.append(humidity_list)
#     sheet.append(wind_list)
#
#     wb.save(excelname.decode("utf-8") + ".xlsx")

def getPositionName(soup, num):
    position_name = soup.find(class_="crumbs")
    name = []
    for i in range(len(position_name.find_all("a"))):
        name.append(position_name.find_all("a")[i].text)
    name.append(position_name.find_all("span")[len(position_name.find_all("span"))-1].text)
    print(num,name)
    # print num,position_name.find_all("a")[0].text,position_name.find_all("span")[0].text, position_name.find_all("a")[1].text,position_name.find_all("span")[1].text,position_name.find_all("span")[2].text
    name_str = "-".join(name)
    print(name_str)
    return name_str
    pass

def save_in_db(num,weather_date, weather_position_name, weather_list, fullName):
    # time_list = [] #小时
    # temperature_list = [] #温度
    # rain_list = []  #降雨量
    # humidity_list = []  #相对湿度
    # windDirection_list = []  #风向
    # windPower_list = []  #风力
    # od23_list = []

    insert_list = []

    for item in weather_list:
        #od21小时，od22温度，od26降雨，od24风向，od25风力
        # time_list.append(item['od21'])
        # temperature_list.append(item['od22'])
        # rain_list.append(item['od26'])
        # humidity_list.append(item['od27'])
        # windDirection_list.append(item['od24'])
        # windPower_list.append(item['od25'])
        # od23_list.append(item['od23'])
        weather_item = {}
        weather_item['time'] = item['od21']
        weather_item['temperature'] = item['od22']
        weather_item['rain'] = item['od26']
        weather_item['humidity'] = item['od27']
        weather_item['windDirection'] = item['od24']
        weather_item['windPower'] = item['od25']
        weather_item['od23'] = item['od23']
        insert_list.append(weather_item)
        # print(item)

    # print (insert_list)

    conn = sqlite3.connect("demo.db")
    c = conn.cursor()
    for item in insert_list:

        sql = "insert into weather (positionId,name,rain,humidity,windDirection,windPower,date_time,fullName) \
            values (num,weather_position_name,)"
        c.execute("insert into weather (positionId,name,date_time,temperature,rain,humidity,windDirection,windPower,fullName) \
            values(?,?,?,?,?,?,?,?,?)",(num,weather_position_name,item['time'],item['temperature'],item['rain'],item['humidity'],item['windDirection'],item['windPower'],fullName))
    conn.commit()
    conn.close()





def spider(url,num):
    weather24 = {}
    # url="http://www.weather.com.cn/weather1d/101200302.shtml"
    # url = "http://www.weather.com.cn/weather1d/101200101.shtml"

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser',from_encoding='utf-8')
    # print html
    # print soup.find(class_="ctop")
    # print len(soup.findAll('div',class_="crumbs"))
    if (soup.find(class_="crumbs") == None):
        print(num,"none")
        return False

    res_data = soup.findAll('script')
    # print res_data
    weather_data = res_data[4]
    if(weather_data.text.find("observe24h_data") ==-1):
        weather_data = res_data[5]
        if(weather_data.text.find("observe24h_data") == -1):
            return False
    # print(weather_data)
    fullName = getPositionName(soup, num)

    for x in weather_data:
        weather1 = x
    index_start = weather1.find("{")
    index_end = weather1.find(";")
    weather_str = weather1[index_start:index_end]

    weather = eval(weather_str)

    weather_dict = weather["od"]

    weather_date = weather_dict["od0"]
    weather_position_name = weather_dict["od1"]
    weather_list = list(reversed(weather["od"]["od2"]))

    # save_as_excel(weather_date, weather_position_name, weather_list)
    save_in_db(num,weather_date, weather_position_name, weather_list, fullName)
    return True

def start():
    base_url = "http://www.weather.com.cn/weather1d/101"  # 101200302
    province_num = 30
    city_num = 1
    # position_num = 1
    # num_str = str(province_num).zfill(3) + str(city_num).zfill(2) + str(position_num).zfill(2)
    # url = base_url + num_str + ".shtml"


    while (province_num < 80):
        flag = True
        city_num = 1
        while (city_num < 20):
            position_num = 1
            # if(city_num < 5):
            #     position_num = 0
            # else:
            #     position_num = 1
            while (position_num < 30):
                num_str = str(province_num).zfill(2) + str(city_num).zfill(2) + str(position_num).zfill(2)
                url = base_url + num_str + ".shtml"
                # time.sleep(2)
                print(url)
                flag = spider(url, num_str)
                if (flag == False):
                    break
                position_num += 1
                pass
            if (flag == False and position_num == 1):
                break
            city_num += 1
            # position_num = 1
            pass
        if (flag == False and position_num == 1 and city_num == 1):
            # print("********")
            break
        province_num += 1
        # city_num = 1
        # position_num = 1
    pass




if __name__ == "__main__":

    #http://www.weather.com.cn/weather1d/101200101.shtml wuhan
    #http://www.weather.com.cn/weather1d/10120090801A.shtml jingdian
    # spider("http://www.weather.com.cn/weather1d/101200302.shtml",1200302)
    # spider("http://www.weather.com.cn/weather/101200101.shtml",1200101)
    start()
    # num_list = [0, 1, 2, 3, 4, 5]
    # print(num_list[])
    # spider("111",101200101)
#pyinstaller -w -F spider.py

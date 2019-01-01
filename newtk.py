#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-01 09:36:37
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import os
import email2
import schedule
import time
import logging
from fake_useragent import UserAgent
import requests
import json


fake_ua_path = "useragent.json"
ua = UserAgent(path = fake_ua_path)


def get_num(date,from_s,to_s):
	dic = {}
	agt = ua.random
	cookies = "JSESSIONID=A55AF1A9B180B07AB6135D3F4C948BD1; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u79E6%u7687%u5C9B%2CQTP; _jc_save_toStation=%u6F4D%u574A%2CWFK; RAIL_EXPIRATION=1546541865708; RAIL_DEVICEID=Vcqkb2Gdw-FFp42SBgb4dmhCCh-2T7sfz7GZlX0XytIqDQTdzMa8HmGMBsIfwmt1hggPMrouF2nH9zWsPLQaaV3vrFfPUzWkjCv2zc5hdsF7CNmRFJ6WTa6IHQTucxU6wFUpuHJWI1pMY8UI8ued3r4xMbbIR2_Z; _jc_save_toDate=2019-01-01; _jc_save_fromDate=2019-01-10; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=49283594.64545.0000"
	head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': agt,
	'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
	"Cookie":cookies
	}

	with requests.Session() as s:
		for sgdate in date:
			url=('http://kyfw.12306.cn/otn/leftTicket/queryZ?'
		         'leftTicketDTO.train_date={}&'
		         'leftTicketDTO.from_station={}&'
		         'leftTicketDTO.to_station={}&'
		         'purpose_codes=ADULT').format(sgdate,from_s,to_s)
			res = s.get(url,headers = head,verify=False)
			res.encoding = "utf-8"
			print("{}===>{}".format(res.text[:10],agt[:10]))
			try:
				jsons = json.loads(res.text)
				data1 = jsons["data"]["result"][2]
				data = data1.split("|")
				print("{},{},{}".format(data[3],data[28],data[29]))
				dic[sgdate] = [data[3],data[28],data[29]]
				#return data[3],data[28],data[29]
			except BaseException as err:
				dic[sgdate] = ["--","--","--"]
			time.sleep(5)
	return dic

def job():
	try:
		print("job doing")
		datesum = ["2019-01-05","2019-01-06","2019-01-07","2019-01-08","2019-01-09","2019-01-10","2019-01-11","2019-01-12"]
		logging.basicConfig(level=logging.INFO)#,filename="{}log.txt".format(time.strftime("%m-%d")))
		dic = get_num(datesum, "QTP","WFK")
		with open("{}.txt".format(time.strftime("%m-%d")),"a",encoding="utf-8") as tklog:
			for date in datesum:
				tklog.write("{}-{}-{}-{}-{} \n".format(date,time.strftime("%H:%M"),dic[date][0],dic[date][1],dic[date][2]))

	except BaseException as err:
		logging.info("{},Error in job!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in job!==>{}".format(err))

'''
		for date in datesum:
			checi,yw,yz = get_num(date, "QTP","WFK")
			with open("{}.txt".format(time.strftime("%m-%d")),"a",encoding="utf-8") as tklog:
				tklog.write("{}-{}-{}-{}-{} \n".format(date,time.strftime("%H:%M"),checi,yw,yz))
			logging.info("{}-{}-{}-{}-{}".format(date,time.strftime("%H:%M"),checi,yw,yz))
			time.sleep(5)
	except BaseException as err:
		logging.info("{},Error in job!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in job!==>{}".format(err))'''
def sd_mail():
	email2.sendmail(content="{}".format(time.strftime('%y-%m-%d')),file ="{}.txt".format(time.strftime("%m-%d")))



schedule.every().day.at("22:55").do(sd_mail)
schedule.every(1).minutes.do(job)

while 1:
	print("waiting..{}".format(time.strftime('%H:%M:%S')))
	while int(time.strftime('%H%M')) <= 2258 and int(time.strftime('%H%M')) >= 600:
		schedule.run_pending()
		time.sleep(1)
	time.sleep(60)


'''
if __name__ == '__main__':
	datesum = ["2019-01-05","2019-01-06","2019-01-07","2019-01-08","2019-01-09","2019-01-10","2019-01-11","2019-01-12"]
	#dic = get_num(datesum, "QTP","WFK")
	#print(dic)
	job()
'''









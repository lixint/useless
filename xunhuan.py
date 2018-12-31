#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 20:40:47
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$


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

	agt = ua.random
	
	url=('http://kyfw.12306.cn/otn/leftTicket/queryZ?'
         'leftTicketDTO.train_date={}&'
         'leftTicketDTO.from_station={}&'
         'leftTicketDTO.to_station={}&'
         'purpose_codes=ADULT').format(date,from_s,to_s)

	head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': agt,
	'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
	}

	with requests.Session() as s:
		res = s.get(url,headers = head)  #verify=False
		res.encoding = "utf-8"
	#res = requests.get(url,params=param,headers = head)
	#r = res.text.encode('utf-8')
	print("{}===>{}".format(res.text[:20],agt))

	#print(type(r))
	jsons = json.loads(res.text)


	data1 = jsons["data"]["result"][2]
	data = data1.split("|")

	print("{},{},{}".format(data[3],data[28],data[29]))
	return data[3],data[28],data[29]
	#return res

def job():
	try:
		print("job doing")
		datesum = ["2019-01-05","2019-01-06","2019-01-07","2019-01-08","2019-01-09","2019-01-10","2019-01-11","2019-01-12"]
		logging.basicConfig(level=logging.INFO)#,filename="{}log.txt".format(time.strftime("%m-%d")))
		for date in datesum:
			checi,yw,yz = get_num(date, "QTP","WFK")
			with open("{}.txt".format(time.strftime("%m-%d")),"a",encoding="utf-8") as tklog:
				tklog.write("{}-{}-{}-{}-{} \n".format(date,time.strftime("%H:%M"),checi,yw,yz))
			logging.info("{}-{}-{}-{}-{}".format(date,time.strftime("%H:%M"),checi,yw,yz))
			time.sleep(5)
	except BaseException as err:
		logging.info("{},Error in job!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in job!==>{}".format(err))
def sd_mail():
	email2.sendmail(content="{}".format(time.strftime('%y-%m-%d')),file ="{}.txt".format(time.strftime("%m-%d")))

schedule.every().day.at("22:55").do(sd_mail)
schedule.every(5).minutes.do(job)

while 1:
	print("waiting..{}".format(time.strftime('%H:%M:%S')))
	while int(time.strftime('%H%M')) <= 2258 and int(time.strftime('%H%M')) >= 600:
		schedule.run_pending()
		time.sleep(1)
	time.sleep(60)
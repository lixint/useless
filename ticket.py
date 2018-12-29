#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
#import email2
from fake_useragent import UserAgent


'''ltrain_date='2018-12-28'  #日期
from_station='BXP' 	#出站
to_station='IOQ'   #到站'''
   #票型

def get_num(date,from_s,to_s):

	url=('https://kyfw.12306.cn/otn/leftTicket/queryZ?'
         'leftTicketDTO.train_date={}&'
         'leftTicketDTO.from_station={}&'
         'leftTicketDTO.to_station={}&'
         'purpose_codes=ADULT').format(date,from_s,to_s)

	head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': UserAgent().random,
	'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init'
	}

	with requests.Session() as s:
		res = s.get(url,headers = head)  #verify=False
		res.encoding = "utf-8"
	#res = requests.get(url,params=param,headers = head)
	#r = res.text.encode('utf-8')
	print(res.text)

	#print(type(r))
	jsons = json.loads(res.text)


	data1 = jsons["data"]["result"][2]
	data = data1.split("|")

	print("{},{},{}".format(data[3],data[28],data[29]))
	return data[3],data[28],data[29]
	#return res

	# 3车次，26无座，28硬卧，29硬座
if __name__ == '__main__':
	get_num("2019-01-03","QTP","WFK")

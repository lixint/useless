#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 21:14:10
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import requests
import json


'''	ltrain_date='2019-01-03'  #日期
	from_station='QTP' 	#出站
	to_station='WFK'   #到站

	#ltrain_date=data  #日期
	#from_station=from_s 	#出站
	#to_station=to_s
	purpose_codes='ADULT'
	url = "https://kyfw.12306.cn/otn/leftTicket/queryA"
	param = {
	"leftTicketDTO.train_date":ltrain_date,
	"leftTicketDTO.from_station":from_station,
	"leftTicketDTO.to_station":to_station,
	"purpose_codes":purpose_codes
	}
'''	
def a():

	url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2019-01-16&leftTicketDTO.from_station=QTP&leftTicketDTO.to_station=WFK&purpose_codes=ADULT'
	'''head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
					'Accept-Encoding': 'gzip, deflate',
					'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
					'Cache-Control': 'max-age=0',
					'Connection': 'keep-alive',
					'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
					}'''

	head = {'Connection': 'keep-alive',
		'Cache-Control': 'no-cache',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		'Accept':'*/*',
		'X-Requested-With': 'XMLHttpRequest',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		}
	with requests.Session() as s:
		res = s.get(url,headers = head)
	res.encoding = 'utf-8'
	print(res.text)
	return res
a = a()
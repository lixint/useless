#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 21:14:10
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$


import time
import schedule


def job():
	print("working===>{}".format(time.strftime('%H:%M:%S')))


schedule.every(1).seconds.do(job)

while 1:
	if int(time.strftime('%H%M')) <= 950 and int(time.strftime('%H%M')) >= 947:
		run = True
	elif int(time.strftime('%H%M')) <= 955 and int(time.strftime('%H%M')) >= 953:
		run = True
	else:
		run = False
	print("waiting..{}".format(time.strftime('%H:%M:%S')))
	while run:#int(time.strftime('%H%M')) < 938 and int(time.strftime('%H%M')) >= 936:
		schedule.run_pending()
		time.sleep(1)
	time.sleep(1)

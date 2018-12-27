#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 20:40:47
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import ticket
import email2
import schedule
import time
import logging
time_now = time.strftime('%H:%M:%S')
def job():
	datesum = ["2019-01-05","2019-01-06","2019-01-07","2019-01-08","2019-01-09","2019-01-10","2019-01-11","2019-01-12"]
	logging.basicConfig(level=logging.INFO,filename="{}log.txt".format(time.strftime("%m-%d")))
	for date in datesum:
		checi,yw,yz = ticket.get_num(date, "QTP","WFK")
		with open("{}.txt".format(time.strftime("%m-%d")),"a",encoding="utf-8") as log:
			log.write("{}-{}-{}-{}-{}\n".format(date,time.strftime("%H:%M"),checi,yw,yz))
		logging.info("{}-{}-{}-{}-{}".format(date,time.strftime("%H:%M"),checi,yw,yz))
		time.sleep(5)
schedule.every(5).minutes.do(job)

while 1:
	print("waiting..{}".format(time_now))
	while int(time.strftime('%H%M')) <= 1030 and int(time.strftime('%H%M')) >= 1000:
		schedule.run_pending()
		time.sleep(1)
	time.sleep(60)
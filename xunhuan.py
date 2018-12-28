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

def job():
	try:
		datesum = ["2019-01-05","2019-01-06","2019-01-07","2019-01-08","2019-01-09","2019-01-10","2019-01-11","2019-01-12"]
		logging.basicConfig(level=logging.INFO,filename="{}log.txt".format(time.strftime("%m-%d")))
		for date in datesum:
			checi,yw,yz = ticket.get_num(date, "QTP","WFK")
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
	while int(time.strftime('%H%M')) <= 2300 and int(time.strftime('%H%M')) >= 610:
		schedule.run_pending()
		time.sleep(1)
	time.sleep(60)
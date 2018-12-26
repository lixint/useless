#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 21:14:10
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import schedule
import time
import email2
import xunhuan


schedule.every().day.at("06:10").do(xunhuan.sch())

while 1:
	schedule.run_pending()
	time.sleep(1)

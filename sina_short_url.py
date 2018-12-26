#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-10 20:18:26
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import os
import sys
import requests
import webbrowser
import json
from configparser import ConfigParser


conf = ConfigParser()
url = "https://api.weibo.com/2/short_url/shorten.json"
code_url = "https://api.weibo.com/oauth2/authorize"
token_url = "https://api.weibo.com/oauth2/access_token"
'''
redirect_uri = "https://api.weibo.com/oauth2/default.html"
appkey = "4006857088"  # 必填
appsecret = "84196487bc6efc7527d64460cce695d8"  # 必填
'''
def conf_regular():
	global redirect_uri, appkey, appsecret
	try:

		redirect_uri = input("redirect_uri")
		appkey = input("appkey")
		appsecret = input("appsecret")

		conf.read("SinaConfig.ini")
		if not conf.has_section("sina"):
			conf.add_section("sina")
		conf.set("sina", "redirect_uri",redirect_uri)
		conf.set("sina", "appkey",appkey)
		conf.set("sina", "appsecret",appsecret)
		conf.write(open("SinaConfig.ini","w"))

	except BaseException as err:
		print("error in get conf_regular,{}".format(err))




#获取code
def get_code():
	global redirect_uri, appkey, appsecret
	try:
		conf.read("SinaConfig.ini")
		redirect_uri = conf.get("sina", "redirect_uri")
		appkey = conf.get("sina", "appkey")
		appsecret = conf.get("sina", "appsecret")

		weburl = code_url + "?" + "client_id=" + appkey + "&response_type=code&redirect_uri=" + redirect_uri 
		webbrowser.open_new_tab(weburl)
		code = input("Please input the code:")
		return code
	except BaseException as err:
		print("error in get code,{}".format(err))
# 获取token
def get_token(code):
	global redirect_uri, appkey, appsecret
	try:
		params = {"client_id":appkey,"client_secret":appsecret,"grant_type":"authorization_code","redirect_uri":redirect_uri,"code":code}
		data = requests.post(token_url,params = params)
		token_ori = json.loads(data.text)
		token = token_ori["access_token"]
		conf_token(token)
		return token
	except BaseException as err:
		print("error in get token,{}".format(err))
#获取短链接
def get_short_url(token,url_long):
	try:
		access_token = token
		url_long = url_long
		data = requests.get(url,params={"url_long": url_long , "access_token":access_token})
		url_data = json.loads(data.text)
		#url_short = url_data["urls"][0]["url_short"]
		#return url_short
		return url_data   #["urls"]
	except BaseException as err:
		print("error in get short url,{}".format(err))

#配置写
def conf_token(token):
	try:
		conf.read("SinaConfig.ini")
		if not conf.has_section("sina"):
			conf.add_section("sina")
		conf.set("sina", "token",token)
		conf.write(open("SinaConfig.ini","w"))
	except BaseException as err:
		print("error in get conf_token,{}".format(err))




#主函数
def main(url_long):
	
	
	test_url = "https://lixint.me"
	try:
		
		if not os.path.exists('SinaConfig.ini'):
			with open("SinaConfig.ini","w") as c_1:
				conf_regular()
		conf.read("SinaConfig.ini")
		token = conf.get("sina", "token")
		get_short_url(token, test_url)
	except:
		code = get_code()
		token = get_token(code)
		url_short = get_short_url(token, url_long)
		return url_short
		#print(url_short)
	else:
	#conf_regular()
		url_short = get_short_url(token, url_long)
		#print(url_short)
		return url_short
		#for i in range(len(url_short)):
			#print(url_short[i])

		



if __name__ == '__main__':
	url_long = "https://lixint.me"
	main(url_long)
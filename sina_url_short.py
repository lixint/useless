#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-10 20:18:26
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# 放弃了，每次都要登录，没啥卵用。
import os
import webbrowser
import requests
import json
from configparser import ConfigParser

conf = ConfigParser()
if not os.path.exists('SinaConf.ini'):
	with open("SinaConf.ini") as file:
		pass

code_url = "https://api.weibo.com/oauth2/authorize"
token_url = "https://api.weibo.com/oauth2/access_token"


redirect_uri = ""
appkey = ""  # 必填
appsecret = ""  # 必填

code = "cc1bd7c5ced4cd3086b10d771e7b37"

# 获取code
def get_code(code_url):
	weburl = code_url + "?" + "client_id=" + appkey + "&response_type=code&redirect_uri=" + redirect_uri 
	webbrowser.open_new_tab(weburl)

# 获取access_token
def get_token(code):
	
	params = {"client_id":appkey,"client_secret":appsecret,"grant_type":"authorization_code","redirect_uri":redirect_uri,"code":code}
	data = requests.post(token_url,params = params)
	token = json.loads(data.text)

	#print(token["access_token"])
	try:
		token = token["access_token"]
		return token

	except:
		token = 0
		return token

#获取短链接
def get_short_url(token,url_long):
	url = "https://api.weibo.com/2/short_url/shorten.json"
	access_token = token
	url_long = url_long
	data = requests.get(url,params={"url_long": url_long , "access_token":access_token})
	url_short = json.loads(data.text)
	return url_short
	
def main(url_long):
	global code
	if code:
		token = get_token(code)
		if "invalid" in token:
			get_code(code_url)
			new_code = imput("please input new code:")		
		else:
			print(token)
			short_url = get_short_url(token,url_long)
			print(short_url["urls"][0]["url_short"])
	else:
		get_code(code_url)

if __name__ == '__main__':
	url_long = "https://www.lixint.me"
	main(url_long)
	
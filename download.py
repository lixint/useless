#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-24 14:05:49
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$

import os
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin


header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

base = "http://www.ieslpod.com"
'''
res = requests.get("http://www.ieslpod.com/Cultural_English/1_60/",headers = header)
res.encoding = 'utf-8'
print(res.text)

with open ("index.html","w",encoding="utf-8") as fie:
	fie.write(res.text)
soup = BeautifulSoup(res.text,"lxml")
#a = soup.find_all("ul", class_ = "duolie")
'''

#获取Cultural English 路径
def getroot():
	res = requests.get(base,headers = header)
	res.encoding = "utf-8"
	#soup = BeautifulSoup(open("root.html",encoding= "utf-8"),"lxml")
	soup = BeautifulSoup(res.text,"lxml")
	data = soup.find_all("ul",class_ = "duolie")
	lis = data[1].find_all("a")  # 0为Daily English
	list1 = []
	for li in lis:
		href = li.get("href")
		url = urljoin(base, href)
		list1.append(url)
	return list1  #返回列表格式



#采集集合页面各期的连接
def getindex(part_url):
	#print(part_url)
	res = requests.get(part_url,headers = header)
	res.encoding = "utf-8"
	soup = BeautifulSoup(res.text,"lxml")
	#soup = BeautifulSoup(open("index.html",encoding = "utf-8"),"lxml")
	data = soup.find_all("div",id = "list")
	apins = data[0].find_all('a')
	href_list = []
	#title_list = []
	with open("index.txt","a",encoding="utf-8") as index:
		for apin in apins:
			href = apin.get("href")
			url = urljoin(base, href)
			href_list.append(url)
			title = apin.string
			index.write("{}\n".format(title))
	#print("{}\n-----{}\n".format(href_list,title_list))
	return href_list  #返回各期完整链接


def getpage(page_url,name):
	res = requests.get(page_url,headers = header)
	res.encoding = "utf-8"
	with open ("{}.html".format(name),"w",encoding="utf-8") as html:
		html.write(res.text)


def getcontent(name):
	soup = BeautifulSoup(open("{}.html".format(name),encoding = "utf-8"),"lxml")
	div = soup.select(".neirong")
	print(type(div[0]))
	a = str(div[0])
	with open("{}_con.html".format(name),"w",encoding="utf-8") as html:
		html.write(a)

def getvideo(name):
	soup = BeautifulSoup(open("{}.html".format(name),encoding = "utf-8"),"lxml")
	content = soup.text
	mpurl = re.findall(r'mp3:"(.*?)"', content)
	url = urljoin(base, mpurl[0])
	#print(url)
	mpp = requests.get(url,stream=True)
	with open('{}.mp3'.format(name),'wb') as mus:
		for chunk in mpp.iter_content(chunk_size=1024):
			if chunk:
				mus.write(chunk)


def main():
	part_urls = getroot()
	#print(part_urls)
	for part_url in [part_urls[0]]:   #[0]为测试用
		#print(part_url)
		href_list = getindex(part_url)
		for i in range(3):
			print("start")
			getpage(href_list[i], i+1)
			getcontent(i+1)
			getvideo(i+1)
			print("{} is done".format(i))
			time.sleep(3)





if __name__ == '__main__':
	#getcontent("content")
	main()
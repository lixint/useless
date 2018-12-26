import wget
import urllib.parse
import os
import requests
import time
import logging
#url = "http://www.ieslpod.com/mp223/52.m4a"
file = "1.txt"
logging.basicConfig(level=logging.INFO,filename="log.txt")
#print(a.path[7:])
'''b = os.path.splitext(a.path)
print(b)'''

'''with open(file,"r",encoding = "utf-8") as files:
	urls = files.readlines()
print(urls[0])'''
#print(urls[53][:-1])
#wget.download(urls[0][:-1])
def download(url):
	try:
		wget.download(url[:-1])
		logging.info("{} download one file".format(time.strftime("%H:%M:%M")))
	except BaseException as err:
		logging.info("{},Error in download!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in download!==>{}".format(err))

def check(url):
	try:
		filedata = urllib.parse.urlsplit(url[:-1])
		filename = filedata.path[7:]
		res = requests.get(url,stream=True)
		websize = res.headers["content-length"]
		#print(type(websize))
		realsize = os.path.getsize(filename)
		#print(type(realsize))
		if int(websize) != int(realsize):
			#print("wrong")
			logging.info("{},{} is redownloading..".format(time.strftime("%H:%M:%M"),filename))
			download(url)
		else:
			logging.info("{} is download complete at {}".format(filename,time.strftime("%H:%M:%M")))
			print("check pass")
	except BaseException as err:
		logging.info("{},Error in check!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in check!==>{}".format(err))

def read(file):
	try:

		with open (file,"r",encoding="utf-8") as f:
			lines = f.readlines()
		return lines
	except BaseException as err:
		logging.info("{},Error in read!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in read!==>{}".format(err))


def main():
	lines = read(file)
	for url in lines:
		download(url)
		check(url)


if __name__ == '__main__':
	#download(url)
	main()
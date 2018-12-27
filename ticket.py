import requests
import json
#import email2


'''ltrain_date='2018-12-28'  #日期
from_station='BXP' 	#出站
to_station='IOQ'   #到站'''
   #票型





def get_num(data,from_s,to_s):


	ltrain_date=data  #日期
	from_station=from_s 	#出站
	to_station=to_s
	purpose_codes='ADULT'
	url = "https://kyfw.12306.cn/otn/leftTicket/queryA"

	param = {
	"leftTicketDTO.train_date":ltrain_date,
	"leftTicketDTO.from_station":from_station,
	"leftTicketDTO.to_station":to_station,
	"purpose_codes":purpose_codes
	}

	head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

	with requests.Session() as s:
		res = s.get(url,params=param,headers = head)
	res.encoding = "utf-8"
	#res = requests.get(url,params=param,headers = head)
	jsons = json.loads(res.text)
	#print(json.dumps(jsons["data"]["result"][2],indent=4,ensure_ascii = False))
	data1 = jsons["data"]["result"][2]
	data = data1.split("|")
	
	#print("{},{}".format(data[3],data[28]))
	'''for i in range(len(data)):
					print("{}==>{}".format(i,data[i]))
			'''
	print("{},{},{}".format(data[3],data[28],data[29]))
	return data[3],data[28],data[29]

	# 3车次，26无座，28硬卧，29硬座
if __name__ == '__main__':
	get_num("2019-01-03","QTP","WFK")

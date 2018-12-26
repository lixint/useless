#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-26 18:58:58
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
# @Version : $Id$
'''
发邮件用的，调用xx.sendmail("内容"),只加内容的话，就发给lixint8，
可以加一个附件，xx.sendmail(content="内容",file="附件",receiver="接收人",title="主题")


'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.header import Header
from smtplib import SMTP_SSL
import time
import os
import logging
logging.basicConfig(level=logging.INFO,filename="email_log.txt")
is_exist = os.path.exists
host_server = 'smtp.126.com'
sender = 'lxt69826400@126.com'
pwd = 'Li930121'

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send_content(content,receiver,title):
	#登录
	try:
		smtp = SMTP_SSL(host_server)
		#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
		smtp.set_debuglevel(0)
		smtp.ehlo(host_server)
		smtp.login(sender, pwd)

		msg = MIMEText(content, "plain", 'utf-8')
		msg["Subject"] = Header(title, 'utf-8').encode()
		msg["From"] = _format_addr('Machine {}'.format(sender))
		msg["To"] = _format_addr('Dear {}'.format(receiver)) ## 接收者的别名

		smtp.sendmail(sender, receiver, msg.as_string())
		smtp.quit()
	except BaseException as err:
		logging.info("{},Error in send_content!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in send_content!==>{}".format(err))


def send_file(contnen,file,receiver,title):
	try:	
		#登录
		smtp = SMTP_SSL(host_server)
		#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
		smtp.set_debuglevel(0)
		smtp.ehlo(host_server)
		smtp.login(sender, pwd)

		msg = MIMEMultipart()
		msg["Subject"] = Header(title, 'utf-8').encode()
		msg["From"] = _format_addr('Machine {}'.format(sender))
		msg["To"] = _format_addr('Dear {}'.format(receiver)) ## 接收者的别名

		msg.attach(MIMEText('content', 'plain', 'utf-8'))

		att = MIMEText(open(file, 'rb').read(), 'base64', 'utf-8')
		
		att.add_header('Content-Disposition', 'attachment', filename=os.path.split(file)[1])
		att.add_header('Content-ID', '<0>')
		att.add_header('X-Attachment-Id', '0')
		msg.attach(att)
		'''with open(file,'rb') as f:
						# 设置附件的MIME和文件名，这里是png类型:
				    	mime = MIMEBase('image', 'png', filename='test.png')
				   		# 加上必要的头信息:
				    	mime.add_header('Content-Disposition', 'attachment', filename='test.png')
				    	mime.add_header('Content-ID', '<0>')
				    	mime.add_header('X-Attachment-Id', '0')
				    	# 把附件的内容读进来:
				    	mime.set_payload(f.read())
				    	# 用Base64编码:
				    	encoders.encode_base64(mime)
				    	# 添加到MIMEMultipart:
				    	msg.attach(mime)'''
		smtp.sendmail(sender, receiver, msg.as_string())
		smtp.quit()
	except BaseException as err:
		logging.info("{},Error in send_file!==>{}".format(time.strftime("%H:%M:%M"),err))
		print("Error in send_file!==>{}".format(err))


def sendmail(content,file = None,receiver = None,title=None):

	host_sever = 'smtp.126.com'
	sender = 'lxt69826400@126.com'
	pwd = 'Li930121'

	content = content 

	if not receiver:
		receiver = 'lixint8@163.com'
	if not title:
		title = "提醒"
	if not content:
		content = "内容未添加"
		logging.info("{} 内容未添加".format(time.strftime("%H:%M:%M")))


	if file and is_exist(file):
		send_file(content,file,receiver,title)
	else:
		send_content(content, receiver, title)


if __name__ == '__main__':
	sendmail("text",file ="1.txt")

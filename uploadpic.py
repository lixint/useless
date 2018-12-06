#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lixint (lixint8@gmail.com)
# @Link    : https://github.com/lixint/
'''
requirements: requests  cos-python-SDK-v5
'''
import re
import requests
import json
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
#import logging
import argparse
import os
import time
import shutil
from urllib import parse
from configparser import ConfigParser



def get_artical_path(art_tittle):
	'''
	合成文章路径
	'''
	try:
		dir_path = os.getcwd()
		#如果是在博客根目录放置脚本，请修改testdir\_posts路径为source\_posts或其他放置文章的目录。
		article_path = os.path.join(dir_path,r"source\_posts",art_tittle)
		return article_path
		print(article_path)
	except BaseException as err:
		print("error in get_artical_path\n{}".format(err))
'''
def pic(pic_origin_url):
	for i in range(len(pic_origin_url)):
		try:
			pic_basename = os.path.basename(pic_origin_url[0])		#获取文章文件名及后缀
			pic_extend = os.path.splitext(pic_basename)[1][1:]
		except:
			pic_extend  = "0"
		if pic_extend in
'''



def change_pic_path(article_path,upld_method):  
	'''
	article_path: 文章的本地路径
	upld_method: 上传方法，sm.ms，腾讯cos，本地（github）。
	'''
	is_exist = os.path.exists
	print("please wait a moment")
	try:
		with open (article_path,'r',encoding = 'utf-8') as md:
			article_content = md.read()
			pic_block = re.findall(r'\!.*?\)',article_content)  #获取添加图片的Markdown文本
			#print(pic_block)
			if upld_method == "smms":
				for i in range(len(pic_block)):
					pic_origin_url = re.findall(r'\((.*?)\)',pic_block[i]) #获取插入图片时图片的位置
					if not is_exist(pic_origin_url[0]):
						continue
					pic_new_url = smms(pic_origin_url[0])
					print("pic_new_url is {}".format(pic_new_url))
					article_content = article_content.replace(pic_origin_url[0],pic_new_url)
			elif upld_method == "tx":
				for i in range(len(pic_block)):
					pic_origin_url = re.findall(r'\((.*?)\)',pic_block[i]) #获取插入图片时图片的位置
					#print("pic_origin_url is {}".format(pic_origin_url))
					if not is_exist(pic_origin_url[0]):
						continue
					pic_new_url = tx(pic_origin_url[0])
					print("pic_new_url is {}".format(pic_new_url))
					article_content = article_content.replace(pic_origin_url[0],pic_new_url)
			elif upld_method == "local":
				for i in range(len(pic_block)):
					pic_origin_url = re.findall(r'\((.*?)\)',pic_block[i]) #获取插入图片时图片的位置
					if not is_exist(pic_origin_url[0]):
						continue
					pic_new_url = local(pic_origin_url[0])
					print("pic_new_url is {}".format(pic_new_url))
					article_content = article_content.replace(pic_origin_url[0],pic_new_url)
			else:
				print("part of get_pic_path error")

		with open (article_path,'w',encoding = 'utf-8') as md:
			md.write(article_content)
		print("job done")

	except BaseException as err:
		print("error in change_pic_path\n{}".format(err))



#上传至SM.MS
def smms(pic_origin_url):
	try:
		smms_url = 'https://sm.ms/api/upload'
		#file_path = r"C:\Users\Root\AppData\Roaming\Typora\typora-user-images\1542107269017.png"   #for test
		data = requests.post(
			smms_url,
			files={'smfile':open(pic_origin_url,'rb'),
			'format':'json'}
		)
		pic_new_url = json.loads(data.text)
		cloud_path = pic_new_url['data']['url'] 
		return(cloud_path)
		
	except BaseException as err:
		print("error in smms\n{}".format(err))

def tx(pic_origin_url):
	'''
	上传至腾讯云
	'''
	try:
		secret_id = tx_s_id	  # 替换为用户的 secretId
		secret_key = tx_s_key	  # 替换为用户的 secretKey
		region = tx_region	 # 替换为用户的 Region
		Bucket = tx_Bucket #替换为用户的Bucket
		token = None				# 使用临时密钥需要传入 Token，默认为空，可不填
		scheme = 'https'			# 指定使用 http/https 协议来访问 COS，默认为 https，可不填
		config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
		client = CosS3Client(config)
	
		pic_basename = os.path.basename(pic_origin_url)		#获取图片文件名及后缀

		time_for_dir = time.strftime("%Y-%m-%d")		#获取当前日期用于命名文件夹

		#获取文章文件名用于创建文件夹
		article_basename = os.path.basename(article_path)		#获取文章文件名及后缀
		article_name = os.path.splitext(article_basename)[0]	#splitext返回（文件名，扩展名的数组），提取文件名



		#默认上传后建立一个以当前日期命名的文件夹，如果不需要，注释掉这一行用下一行。
		#cloud_path = time_for_dir + r'/' + pic_basename

		#上传后建立一个以文件名命名的文件夹，如果不需要，注释掉用下一行
		cloud_path = article_name + r'/' + pic_basename

		#上传至根目录，不创建文件夹
		#cloud_path = pic_basename
		key = cloud_path
	# 2. 获取客户端对象
		with open(pic_origin_url, 'rb') as fp:
			response = client.put_object(
				Bucket=Bucket,
				Body=fp,
				Key=key,
			#StorageClass='STANDARD',
			#ContentType='text/html; 
			#charset='utf-8'
			)
		cloud_path = client._conf.uri(bucket=Bucket, path=key)
		return cloud_path
	except BaseException as err:
		print("error in tx\n{}".format(err))


#用于github page搭建的博客，放到source文件夹
def local(pic_origin_path):
	'''
	本部分没法用，请无视
	修改github_url为 博客的github项目地址，最后要加个 /
	默认在本地项目文件的source文件夹中建立一个blog_img文件夹存储图片

	此部分代码混乱，如有其他需求请自行修改
	'''
	try:
		github_url = "https://github.com/lixint/lixint.github.io/"
		new_path = r"source\blog_img"
		pic_basename = os.path.basename(pic_origin_path)
		isexists = os.path.exists(r"source/blog_img")  #判断目录是否存在

		if not isexists:
			os.mkdir(r"source/blog_img")  #不存在则新建目录
			shutil.move(pic_origin_path,new_path)
		else:
			shutil.move(pic_origin_path,new_path)
		#print("true")
		cloud_path = parse.urljoin(github_url,"blob/master/blog_img/")
		cloud_url = parse.urljoin(cloud_path,pic_basename)
		return(cloud_url)
	except BaseException as err:
		print("error in local\n{}".format(err))


if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(help="commands", dest="command")

	smms_parser = subparsers.add_parser("smms",help="use smms")
	smms_parser.add_argument("art_tittle",help="input filename")

	tx_parser = subparsers.add_parser("tx",help="use tx cos")
	tx_parser.add_argument("art_tittle",help="input filename")

	local_parser = subparsers.add_parser("local",help="use local")
	local_parser.add_argument("art_tittle",help="input filename")

	args = parser.parse_args()


	
	
if args.command == "smms":
	article_path = get_artical_path(args.art_tittle)
	change_pic_path(article_path,'smms')

if args.command == "tx":
	#加载额外存放的腾讯配置文件
	cfg = ConfigParser()
	cfg.read(r'H:\ipuldconf.ini') #可自行修改文件位置

	tx_s_id=cfg.get('tx','secret_id')
	tx_s_key=cfg.get('tx','secret_key')
	tx_region=cfg.get('tx','region')
	tx_Bucket=cfg.get('tx','Bucket')

	article_path = get_artical_path(args.art_tittle)
	change_pic_path(article_path,'tx')

if args.command == "local":
	article_path = get_artical_path(args.art_tittle)
	change_pic_path(article_path,'local')
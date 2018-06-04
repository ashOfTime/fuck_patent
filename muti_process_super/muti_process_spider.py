# -*- coding: utf-8 -*- 
"""
从datetime数据库里取出日期数据、页码信息，返回每一页的详情信息
多进程调用版本
"""
import requests
import pymysql
import json
import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from Login import login
import redis
import logging


from setting import username,password,thread,redis_host,redis_port
from proxy import ProxyPool




def get_data_from_datetime(threads, id_task):
	"""
	从datetime数据库里读日期信息
	"""
	#sql_select = "select * from `2015` where content = 'F'  AND id >= %s and id <= %s limit 0,{} ".format(str(threads))
	sql_select = "select * from `2015` where content = 'F' and id in %s limit {}".format(threads)
	db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
	cursor = db.cursor()
	id_task = tuple(id_task)
	cursor.execute(sql_select, (id_task,))
	t = cursor.fetchall()

	cursor.close()
	db.close()

	return t

def read_cookies_from_local():
	"""
	从本地读cookie
	"""
	with open('cookie_login.json', 'r') as f:
		cookies = json.loads(f.read())

	return cookies

def spider(datetime_info):
	#print(datetime_info)

	id = datetime_info[0]
	print(id)
	datetime = datetime_info[1]
	totalCount = datetime_info[2]
	start = datetime_info[5]
	
	cookies = datetime_info[-2]
	ip = datetime_info[-1]

	proxies={
    'http':'http://{}'.format(ip),
    'https':'https://{}'.format(ip)
                }

	datetime_shit = datetime.replace('-', '.')
	datetime_shit = ['[{}][ ]'.format(s) + '{0,}' for s in datetime_shit]
	datetime_shit = ''.join(datetime_shit)

	headers = {
    'Origin': 'http://www.pss-system.gov.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'text/html, */*; q=0.01',
    'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
	}

	data = [
			('resultPagination.limit', '12'),
			('resultPagination.sumLimit', '10'),
			('resultPagination.start', str(start)),
			('resultPagination.totalCount', str(totalCount)),
			('searchCondition.searchType', 'Sino_foreign'),
			('searchCondition.dbId', 'VDB'),
			('searchCondition.originalLanguage', ''),
			('searchCondition.extendInfo[\'MODE\']', 'MODE_TABLE'),
			('searchCondition.extendInfo[\'STRATEGY\']', 'STRATEGY_CALCULATE'),
			('searchCondition.searchExp', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5={}'.format(datetime)),
			('searchCondition.executableSearchExp', ''),
			('searchCondition.literatureSF', ''),
			('searchCondition.targetLanguage', ''),
			('searchCondition.resultMode', 'SEARCH_MODE'),
			('searchCondition.strategy', ''),
			('searchCondition.searchKeywords', datetime_shit),

	 # ('searchCondition.searchKeywords', '[2][ ]{0,}[0][ ]{0,}[1][ ]{0,}[5][ ]{0,}[.][ ]{0,}[0][ ]{0,}[1][ ]{0,}[.][ ]{0,}[0][ ]{0,}[7][ ]{0,}'),
		]

	try:
		response = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data, proxies=proxies, timeout=20)

		if response.content.decode('utf-8').find('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">') != -1:
			status = 2
			content = 'F'
			print(id,'cc')
		elif response.content.decode('utf-8').find('您的访问出错了') != -1:
			status = 3
			content = 'F'
			print(id,'ii')

		elif response.content.decode('utf-8').find('您的操作太过频繁') != -1:
			status = 3
			content = 'F'
			print(id,' ban')

		elif response.content.decode('utf-8').find('request too fast, please control the request frequency') != -1:
			status = 3
			content = 'F'
			print(id,' ban')

		else:
			status = 1
			content = response.content
			print(id,'**') 
	except:
		content = 'F'
		status = 3

	
	return id,status,content

def write_db(id, content):
	"""
	把爬回来的content信息更新到原来的数据库里
	"""

	sql_update = 'update `2015` set content = %s where id = %s'
	db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
	cursor = db.cursor()

	#print(id)
	#print(content.decode('utf-8'))

	cursor.execute(sql_update,(content,id))
	db.commit()

	cursor.close()
	db.close()

def get_ip_from_proxiesPool():
	proxypool = ProxyPool(redis_host, redis_port)
	is_ip = 0
	while not is_ip:
		try:
			t = proxypool.pop_ip()[0]
			ip = t[0].decode('utf-8')
			timestamp = t[1]

			if time.time() - timestamp > 60:
				print('ip too old')
				time.sleep(1)
			else:
				is_ip = 1
		except Exception as e:
  
			print('ip proxy is empty ,wait.....',e)
			time.sleep(3)

	print(ip)
	return ip,timestamp

def muti_control(id_list):
	
	pool = ThreadPool(7)
	proxypool = ProxyPool(redis_host, redis_port)
	#模拟登陆
	s = requests.Session()
	is_login = 0
	while not is_login:
		ip,timestamp = get_ip_from_proxiesPool()
		is_login = login(s,ip)
		#time.sleep(10)

	print('suss login')
	proxies={
    'http':'http://{}'.format(ip),
    'https':'https://{}'.format(ip)
                }
	requests.post(url='http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/pageIsUesd-pageUsed.shtml',proxies=proxies, cookies=s.cookies)
	print('tou ming zhuang ')

	while True:
#用于记录ip使用次数
		#datetime_info = get_data_from_datetime(threads, sub_duty[0], sub_duty[-1])
		datetime_info = get_data_from_datetime(10, id_list)
		if len(datetime_info) == 0:
			print(time.asctime())
			break
		else:
			task = [list(t) for t in datetime_info]
			for i in task:
				i.append(s.cookies)
				i.append(ip)
			result = pool.map(spider, task)

			#根据返回的结果判断是否需要换Ip、cookies
			needIp = 0
			needCookies = 0

			for r in result:
				#id = r[0]
				#status = r[1]
				#content = r[2]
				if r[1] == 1:
					#正常的数据，写入数据库
					write_db(r[0],r[2])
				elif r[1] == 2:
					#cookies,
					print(r[0],'cookies wrong')
					needCookies = 1
					needIp = 1
				elif r[1] == 3:
					#ip过期
					print(r[0],'ip wrong')
					needIp = 1


			#根据结果 更新session的状态
			if needCookies:
				is_login = 0
				while not is_login:
					print('login again...')
					ip,timestamp = get_ip_from_proxiesPool()
					is_login = login(s,ip)
					requests.post(url='http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/pageIsUesd-pageUsed.shtml',proxies=proxies, cookies=s.cookies)
				print('tou ming zhuang ')
				proxypool.push_ip(ip,timestamp)


			elif needIp:
					while True:
						ip,timestamp = get_ip_from_proxiesPool()
						print('renew ip ...')
						proxies={
					    'http':'http://{}'.format(ip),
					    'https':'https://{}'.format(ip)
		                }

						try:
							rsp_ipTest = requests.get('http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml',proxies=proxies,timeout=10)
							if rsp_ipTest.status_code == 200 and '访问受限' not in rsp_ipTest.text:
								try:
									requests.post(url='http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/pageIsUesd-pageUsed.shtml',proxies=proxies, cookies=s.cookies, timeout=7)
									print('tou ming zhuang ')
									break

								except:
									pass

								
						except:
							pass

		# if go_back_cnt==3:
		# 	proxypool.push_ip(ip,timestamp)


					
#muti_control_2(44000, 45000)
#r = get_data_from_datetime(8, 10000,11000)
#print(r)







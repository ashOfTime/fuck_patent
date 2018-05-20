# -*- coding: utf-8 -*- 
"""
从datetime数据库里取出日期数据、页码信息，返回每一页的详情信息
多线程版本
"""
import requests
import pymysql
import json
import time
from get_cookie import get_cookies
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def get_data_from_datetime(threads):
	"""
	从datetime数据库里读日期信息
	"""
	sql_select = "select * from `2015` where content = 'F' limit 0,{} ".format(str(threads))

	db = pymysql.connect('localhost', 'root', 'password', 'datetime')
	cursor = db.cursor()

	cursor.execute(sql_select)
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
	cookies = datetime_info[-1]
	datetime = datetime_info[1]
	paostdata = datetime_info[-3]
	id = datetime_info[0]

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
	  ('resultPagination.start', str(paostdata)),
	  ('resultPagination.totalCount', '12761'),
	  ('searchCondition.searchType', 'Sino_foreign'),
	  ('searchCondition.dbId', ''),
	  ('searchCondition.originalLanguage', ''),
	  ('searchCondition.extendInfo[\'MODE\']', 'MODE_TABLE'),
	  ('searchCondition.extendInfo[\'STRATEGY\']', 'STRATEGY_CALCULATE'),
	  ('searchCondition.searchExp', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5={}'.format(datetime)),
	  ('wee.bizlog.modulelevel', '0200201'),
	  ('searchCondition.targetLanguage', ''),
	  ('searchCondition.executableSearchExp', 'VDB:(PD=\'{}\')'.format(datetime)),
	  ('searchCondition.literatureSF', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5={}'.format(datetime)),
	  ('searchCondition.strategy', ''),
	  ('searchCondition.searchKeywords', ''),
	  #('searchCondition.searchKeywords', '[2][ ]{0,}[0][ ]{0,}[1][ ]{0,}[5][ ]{0,}[.][ ]{0,}[0][ ]{0,}[1][ ]{0,}[.][ ]{0,}[0][ ]{0,}[1][ ]{0,}'),
	    ('searchCondition.searchKeywords', datetime_shit),
		]

	response = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data)
	#print(response.text)

	if response.text.find('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">') != -1:
		status = 2
		content = 'F'
	else:
		status = 1
		content = response.content


	return id,status,content

def write_db(id, content):
	"""
	把爬回来的content信息更新到原来的数据库里
	"""
	sql_update = 'update `2015` set content = %s where id = %s'
	db = pymysql.connect('localhost', 'root', 'password', 'datetime')
	cursor = db.cursor()

	# print(id)
	# print(content.decode('utf-8'))

	cursor.execute(sql_update,(content,id))
	db.commit()

	cursor.close()
	db.close()

def muti_control():

	threads = 5#线程的数目
	datetime_info = get_data_from_datetime(threads)#按照线程数目从数据库里读出需要爬的数据
	pool = ThreadPool(threads)

	cookies = read_cookies_from_local()
	#转成列表形式，并加入cookie信息
	datetime_info = [list(t) for t in datetime_info]
	for i in datetime_info:
		i.append(cookies)

	result = pool.map(spider, datetime_info)

	renew_cookies = 0#是否更新cookies的标志位，默认是0，即不更新
	for r in result:
		print('id is {}'.format(r[0]))
		#对返回的数据，如果status是1的话就写入数据库，否则不动，并且把cookie更新标志位置为1
		if r[1] == 1:
			print('content ok')
			write_db(r[0], r[2])
		elif r[1] == 2:
			print('content no ok')
			renew_cookies = 1
	if renew_cookies:
		get_cookies('keen123', 'keen123')

def main():
	while True:
		muti_control()
		time.sleep(5.5)
# if __name__ == '__mann__':
# 	main()






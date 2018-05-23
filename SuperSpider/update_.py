"""
万恶的国网更新了，返回的数据变成json格式的了，为了保持数据的一致性，把之前保存的二进制的content文件重新爬取，变成json格式

"""



import requests
import pymysql
import json
from get_cookie import get_cookies


def get_data_from_datetime():
	"""
	从datetime数据库里读日期信息
	"""
	sql_select = "select * from `2015` where content = 'F' limit 1"

	db = pymysql.connect('localhost', 'root', 'password', 'datetime')
	cursor = db.cursor()

	cursor.execute(sql_select)
	t = cursor.fetchone()

	cursor.close()
	db.close()
	print(t)
	return t

def read_cookies_from_local():
	"""
	从本地读cookie
	"""
	with open('cookie_login.json', 'r') as f:
		cookies = json.loads(f.read())

	return cookies

def spider(datetime, start, totalCount, cookies):
	headers = {
	    'Origin': 'http://www.pss-system.gov.cn',
	    'Accept-Encoding': 'gzip, deflate',
	    'Accept-Language': 'zh-CN,zh;q=0.9',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'Accept': 'application/json, text/javascript, */*; q=0.01',
	    'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
	    'X-Requested-With': 'XMLHttpRequest',
	    'Connection': 'keep-alive',
	}

	datetime_shit = datetime.replace('-', '.')
	datetime_shit = ['[{}][ ]'.format(s) + '{0,}' for s in datetime_shit]
	datetime_shit = ''.join(datetime_shit)
	data = [
	  ('resultPagination.limit', '12'),
	  ('resultPagination.sumLimit', '10'),
	  ('resultPagination.start', str(start)),
	  ('resultPagination.totalCount', str(totalCount)),
	  ('searchCondition.searchType', 'Sino_foreign'),
	  ('searchCondition.dbId', 'VDB'),
	  ('searchCondition.originalLanguage', ''),
	  ('searchCondition.extendInfo[\'MODE\']', 'MODE_HISTORY'),
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

	response = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data)
	print(response.json()['searchResultDTO']['searchResultRecord'][0]['recordList'][3]['itemValue'])

	if response.text.find('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">') != -1:
		status = 2
		content = 'F'
	else:
		status = 1
		content = response.content

	return response.content,status

def write_db(id, content):
	"""
	把爬回来的content信息更新到原来的数据库里
	"""
	sql_update = 'update `2015` set content = %s where id = %s'
	db = pymysql.connect('localhost', 'root', 'password', 'datetime')
	cursor = db.cursor()
	cursor.execute(sql_update,(content,id))
	db.commit()

	cursor.close()
	db.close()
	
def control():
	
	cookies = read_cookies_from_local()
	t = get_data_from_datetime()
	datetime = t[1]
	start = t[-2]
	totalCount = t[2]
	print(t[:-1])
	content,status = spider(datetime, start, totalCount, cookies)

	if status == 1:
		print('go to db')
		write_db(t[0], content)
	elif status == 2:
		print('cookies too old')
		get_cookies('keen123', 'keen123')


if __name__ == '__main__':
	#get_cookies('keen123', 'keen123')
	get_data_from_datetime()
	#control()
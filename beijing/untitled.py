import requests
import bs4
import pymysql
from math import ceil
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
"""
从北京专利网爬取数据
"""

def create_datetime_db(datetime, allNum):
  """
  提前知道这个网站对某个日期范围一共提供多少个数据，根据这个数据生成任务队列
  datetime:日期
  allNum:一共有多少数据
  """
  db = pymysql.connect('localhost', 'root', 'password', 'beijing')
  cur = db.cursor()
  allPage = allNum
  sql_insert = 'insert into content  values (%s,%s,%s,%s)'
  allPage = ceil(allNum/50)

  for page in range(allPage):
    print(page+1)
    cur.execute(sql_insert, [None, datetime, page+1, 'F'])
    db.commit()
    

  cur.close()
  db.close()

def get_detail():
  year_start = 20170101
  year_end = 20171231
  page = 1
  headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Origin': 'http://search.beijingip.cn',
      'Upgrade-Insecure-Requests': '1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Referer': 'http://search.beijingip.cn/search/search/result?s=((PD%3E=20160101)%20AND%20(PD%3C=20161231))',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
  }

  params = (
      ('s', '((PD>={}) AND (PD<={}))'.format(year_start, year_end)),
  )

  data = [
    ('xd_use_expand', 'false'),
    ('ifsynonymexpand', 'false'),
    ('ifenterprisenameexpand', 'false'),
    ('ifnomalize', '0'),
    ('ifzhineng', '0'),
    ('searchstr', '((PD%3E={})%20AND%20(PD%3C={}))'.format(year_start, year_end) ),
    ('page', str(page)),
    ('stype', '0'),
    ('opnum', '1'),
    ('guojialist', ''),
    ('perpage', '50'),
    ('pn', ''),
    ('mid', ''),
    ('an', ''),
    ('num', ''),
    ('maxPage', '128129'),
    ('cnt', '6406426'),
    ('idisp_words', ''),
    ('sortby', 'XGD|0'),
    ('isdownload', ''),
    ('downloadcurpage', ''),
    ('downloadstartpage', ''),
    ('downloadendpage', ''),
    ('downloadfields', ''),
    ('downloadtype', ''),
    ('downloadtypelist', ''),
    ('saveexp', '0'),
    ('addedCount', '0'),
    ('addedValue', ' '),
    ('addedTitle', ' '),
    ('addedFolderName', ''),
    ('leftFilterShow', ''),
    ('leftFilterQuery', ''),
    ('centerFilterQuery', ''),
    ('centerFilterShow', '0'),
    ('filteredQ', ''),
    ('leftFilterCurr', ''),
    ('originTC', '6406426'),
    ('customfield', 'TI,LS,PA,AN,AD,PN,PD,AB,ZYFT,PC,AGC,AGT,PR,IPCR,IPC,AU,ADDR'),
    ('viewresultzoneonly', ''),
  ]

  response = requests.post('http://search.beijingip.cn/search/search/result', headers=headers, params=params,  data=data)
  return response.content
  # soup = bs4.BeautifulSoup(response.content, 'html.parser')
  # divs = soup.find_all('div', class_='txt_wr')
  # print(divs[0].get_text())

def get_content():
    
  guangdong = GuangDong()
  guangdong.login('441045808@qq.com', 'Woaixuexi@123')

  db = pymysql.connect('localhost', 'root', 'password', 'beijing')
  cursor = db.cursor()
  sql_select = "select * from content where content = 'F' limit 0,1"
  sql_update = "update content set content = %s where id =%s"
  cursor.execute(sql_select)
  t = cursor.fetchone()
  content = guangdong.get_detai(t[1].split('#')[0], t[1].split('#')[1], t[-2])
  cursor.execute(sql_update,(content,t[0]))
  db.commit()

  cursor.close()
  db.close()

def get_datetime(num=8):
  """
  根据线程数目，从数据库里取出数据
  num:线程数目
  """
  db = pymysql.connect('localhost', 'root', 'password', 'beijing')
  cursor = db.cursor()
  sql_select = "select * from content where content = 'F' limit 0,{}".format(num)
  cursor.execute(sql_select)
  t = cursor.fetchall()

  return t

def get_detail(post_data):
  id = post_data[0]
  year_start = post_data[1].split('#')[0]
  year_end = post_data[1].split('#')[1]
  pageNo = post_data[2]
  pageNo = post_data
  headers = {
      'Connection': 'keep-alive',
      'Cache-Control': 'max-age=0',
      'Origin': 'http://search.beijingip.cn',
      'Upgrade-Insecure-Requests': '1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Referer': 'http://search.beijingip.cn/search/search/result?s=((PD%3E=20160101)%20AND%20(PD%3C=20161231))',
      'Accept-Encoding': 'gzip, deflate',
      'Accept-Language': 'zh-CN,zh;q=0.9',
  }

  params = (
      ('s', '((PD>=20160101) AND (PD<=20161231))'),
  )

  data = [
    ('xd_use_expand', 'false'),
    ('ifsynonymexpand', 'false'),
    ('ifenterprisenameexpand', 'false'),
    ('ifnomalize', '0'),
    ('ifzhineng', '0'),
    ('searchstr', '((PD>=20160101) AND (PD<=20161231))'),
    ('page', str(pageNo)),
    ('stype', '0'),
    ('opnum', '1'),
    ('guojialist', ''),
    ('perpage', '50'),
    ('pn', ''),
    ('mid', ''),
    ('an', ''),
    ('num', ''),
    ('maxPage', '128139'),
    ('cnt', '6406904'),
    ('idisp_words', ''),
    ('sortby', 'XGD|0'),
    ('isdownload', ''),
    ('downloadcurpage', ''),
    ('downloadstartpage', ''),
    ('downloadendpage', ''),
    ('downloadfields', ''),
    ('downloadtype', ''),
    ('downloadtypelist', ''),
    ('saveexp', '0'),
    ('addedCount', '0'),
    ('addedValue', ' '),
    ('addedTitle', ' '),
    ('addedFolderName', ''),
    ('leftFilterShow', ''),
    ('leftFilterQuery', ''),
    ('centerFilterQuery', ''),
    ('centerFilterShow', '0'),
    ('filteredQ', ''),
    ('leftFilterCurr', ''),
    ('originTC', '6406904'),
    ('customfield', 'TI,LS,PA,AN,AD,PN,PD,AB,ZYFT'),
    ('viewresultzoneonly', ''),
    ('opkey1', 'ZNJS'),
    ('opv1', ''),
    ('op1', 'AND'),
  ]

  response = requests.post('http://search.beijingip.cn/search/search/result', headers=headers, params=params, data=data)
  return response.content,id

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('http://search.beijingip.cn/search/search/result?s=((PD%3E=20160101)%20AND%20(PD%3C=20161231))', headers=headers, cookies=cookies, data=data)


 

def write_db(result):
  """
  爬回来的二进制数据，更新数据库的字段
  """
  db = pymysql.connect('localhost', 'root', 'password', 'beijing')
  cursor = db.cursor()
  id = result[-1]
  content = result[0]
  print(content.decode('utf-8'))
  sql_update = "update content set content = %s where id =%s"
  cursor.execute(sql_update,(content,id))
  db.commit()

def control():
  """
  中央控制
  """
  threads = 5#线程数目，以及一次从数据库里读取多少个任务数

  
  task = list(get_datetime(threads))
  print(task)
  #多线程，爬
  pool = ThreadPool(threads)
  result = pool.map(get_detail, task)

  status = 0
  for r in result:
    print(r[-1])
    write_db(r)

control()

    

#create_datetime_db('2016.01.01#2016.12.31',6406426)

import requests
import bs4

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

def create_datetime_db(datetime, allNum):
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
  cookies = post_data[-1]
  headers = {
        'Origin': 'http://www.cnipsun.com',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'http://www.cnipsun.com/patent/searchResult.do',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

  data = [
    ('searchExpression', '  \u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5=\'{}\' to \'{}\''.format(year_start, year_end) ),
    ('searchExpressionDesc', '  \u516C\u5F00\u65E5=\'{}\' to \'{}\''.format(year_start, year_end) ),
    ('sortMethod', ''),
    ('ascOrder', ''),
    ('cnSources', 'fmzl_ft,syxx_ft,wgzl_ab,fmsq_ft'),
    ('woSources', 'twpatent,hkpatent'),
    ('field1', '0'),
    ('field1Val', ''),
    ('field2', '0'),
    ('field2Val', ''),
    ('field3', '0'),
    ('field3Val', ''),
    ('pageNo', str(pageNo)),
    ('pageSize', '40'),
          ]

  response = requests.post('http://www.cnipsun.com/patent/search.do', headers=headers,  data=data, cookies=cookies)
  return response.content,id

def write_db(result):
  db = pymysql.connect('localhost', 'root', 'password', 'beijing')
  cursor = db.cursor()
  id = result[-1]
  content = result[0]
  sql_update = "update content set content = %s where id =%s"
  cursor.execute(sql_update,(content,id))
  db.commit()

def control():
  """
  中央控制
  """
  threads = 8#线程数目，以及一次从数据库里读取多少个任务数

  #读取cookies
  #把cookies和post_data拼接起来，发个spider
  task = list(get_datetime(threads))
  task = [list(i)  for i in task]
  #多线程，爬
  pool = ThreadPool(threads)
  result = pool.map(get_detail, task)

  #用于判断返回的值是否正常，正常则写入数据库，否则做相应的更新
  #status=0 正常
  #status=2 登陆过期
  status = 0
  for r in result:
    print(r[-1])
    write_db(r)
    # if '请输入注册邮箱' in r[0].decode('utf-8'):
    #   print('login outof time')
    #   status = 2
    # else:
    #   write_db(r)



    


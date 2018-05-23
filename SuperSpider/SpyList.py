# -*- coding: utf-8 -*-
"""
创建待爬取的数据库。
每次post一个日期过去，返回的结果里有这个日期下有多少个记录、多少页。有多少页就新建多少个字段，每个字段里先填入为了要获取详情信息需要post的字段。
"""
import pymysql
import requests
import bs4
import re
import datetime
import time

#AttributeError: 'NoneType' object has no attribute 'get_text'
sql_insert = 'INSERT INTO `2015` VALUES (%s,%s,%s,%s,%s,%s,%s)'

def getTotal(date_time):
  cookies = {
    'WEE_SID': 'b3IA0wp8kT4mPsovOEmpFHebkvmFDHHQXQQtEzozt1a_DdYJu6UR!1514216131!158272934!1524727220860',
    'IS_LOGIN': 'true',
    'avoid_declare': 'declare_pass',
    'JSESSIONID': 'b3IA0wp8kT4mPsovOEmpFHebkvmFDHHQXQQtEzozt1a_DdYJu6UR!1514216131!158272934',
}


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
    ('searchCondition.searchExp', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5={}'.format(date_time)),
    ('searchCondition.dbId', 'VDB'),
    ('searchCondition.searchType', 'Sino_foreign'),
    ('searchCondition.extendInfo[\'MODE\']', 'MODE_TABLE'),
    ('searchCondition.extendInfo[\'STRATEGY\']', 'STRATEGY_CALCULATE'),
    ('searchCondition.originalLanguage', ''),
    ('searchCondition.targetLanguage', ''),
    ('wee.bizlog.modulelevel', '0200201'),
    ('resultPagination.limit', '12'),
  ]


  response = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0402-executeCommandSearch.shtml', headers=headers, cookies=cookies, data=data)
  
  if response.text.find('没有检索到') != -1:
    #如果网页里有 没有检索到，说明这一页没有查到
    total_page =0
    total_cnt=0
  else:
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    input_tag = soup.find('div', class_='page_top')
    s = input_tag.get_text()

    pattern = re.compile(r'共(.*)页(.*)条数据')
    result = re.findall(pattern, s)[0]
    total_page = int(result[0])
    total_cnt=int(result[1])
    

  return total_page,total_cnt

def toSpyList(date_time):
  db = pymysql.connect('localhost', 'root', 'password', 'patent_datetime')
  cursor = db.cursor()

  #爬取查询日期下一共有多少个专利，这些专利有多少页
  print('query the info of ',date_time)
  total_page,total_cnt = getTotal(date_time)
  print('the total_page is {}, the total_cnt is {}'.format(total_page,total_cnt))

  print('build {} query list'.format(date_time))

  if total_cnt==0 and total_page==0:
    #如果这两个数字为0，说明该日期下检索到的结果为0，插入的数据全是0
    print('empty day')
    cursor.execute(sql_insert,(None,date_time, total_cnt, total_page, 0, 0, 'F'))
    db.commit()
  else:
    for cur_page in range(total_page):
      if cur_page%100 == 0:
        print(cur_page)
      poat_data = 12*cur_page
      cursor.execute(sql_insert,(None,date_time, total_cnt, total_page, cur_page+1, poat_data, 'F'))
      db.commit()

  cursor.close()
  db.close()

def datelist(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    result = []
    curr_date = start_date
    while curr_date != end_date:
        result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
        curr_date += datetime.timedelta(1)
    result.append("%04d-%02d-%02d" % (curr_date.year, curr_date.month, curr_date.day))
    return result

l = datelist((2015,1,1),(2016,1,1))
for i in l:
  toSpyList(i)
  time.sleep(3)

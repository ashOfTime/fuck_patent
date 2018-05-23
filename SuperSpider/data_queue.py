import json
import requests
import sys
import get_cookie





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



#get_cookie.get_cookies('keen123','keen123')
# with open('/Users/xuweikang/yancheng_project/data_queue/cookie_login.json','r') as f:
# 	cookies = json.loads(f.read())
# print(cookies)

# headers = {
#     'Origin': 'http://www.pss-system.gov.cn',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'Accept': 'text/html, */*; q=0.01',
#     'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Connection': 'keep-alive',
# }

# data = [
#   ('resultPagination.limit', '12'),
#   ('resultPagination.sumLimit', '10'),
#   ('resultPagination.sumLimit', '10'),
#   ('resultPagination.start', '0'),
#   ('resultPagination.totalCount', '9246'),
#   ('searchCondition.searchType', 'Sino_foreign'),
#   ('searchCondition.dbId', ''),
#   ('searchCondition.extendInfo[\'STRATEGY\']', 'STRATEGY_CALCULATE'),
#   ('searchCondition.strategy', ''),
#   ('searchCondition.literatureSF', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5=2015-03-02'),
#   ('searchCondition.targetLanguage', ''),
#   ('searchCondition.originalLanguage', ''),
#   ('searchCondition.extendInfo[\'MODE\']', 'MODE_TABLE'),
#   ('searchCondition.searchExp', '\u516C\u5F00\uFF08\u516C\u544A\uFF09\u65E5=2015-03-02'),
#   ('searchCondition.executableSearchExp', 'VDB:(PD=\'2015-03-02\')'),
#   ('wee.bizlog.modulelevel', '0200201'),
#   ('searchCondition.searchKeywords', '[2][ ]{0,}[0][ ]{0,}[1][ ]{0,}[5][ ]{0,}[.][ ]{0,}[0][ ]{0,}[3][ ]{0,}[.][ ]{0,}[0][ ]{0,}[2][ ]{0,}'),
# ]

# response = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml', headers=headers, cookies=cookies, data=data)
# print(response.text)
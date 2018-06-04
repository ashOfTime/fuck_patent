
import pymysql
import json
import sys



id = sys.argv[1]

sql_select = 'SELECT * FROM datetime.`2015` where id = %s'

db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
cursor = db.cursor()
cursor.execute(sql_select,id)
t = cursor.fetchone()

content = t[-1].decode('utf-8')

print(t[:-1])
print(content)
#print('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">' in content)


cursor.close()
db.close()

#10:36 1000个 	直接从网上请求ip 10min
#10:50 1000个  	代理池        20min
#11:11 1000   	代理池        16min
#11:44 1000     api      
#12：38 26000 2000ge

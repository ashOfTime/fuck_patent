
import pymysql
import json

id = 1
sql_select = 'SELECT * FROM datetime.`2015` where id = %s'

db = pymysql.connect('localhost', 'root', 'password', 'datetime')
cursor = db.cursor()
cursor.execute(sql_select,id)
t = cursor.fetchone()
id  = t[0]
content = t[-1].decode('utf-8')

print(t[:-1])
print(t[-1])


cursor.close()
db.close()
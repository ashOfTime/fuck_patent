import pymysql
import json
import sys
db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
cursor = db.cursor()

id_start = sys.argv[1]
id_range = sys.argv[2]
sql_select = "select id,content from `2015` where content != 'F' and id >{} limit {}".format(id_start, id_range)
num = cursor.execute(sql_select)
for _ in range(num):
	t = cursor.fetchone()
	id = t[0]
	content = t[1]
	#print(id)
	try:
		json.loads(content)
	except Exception as e:
		print(content)
		print(id,'wrong')

import pymysql
import time
sql_select = "SELECT id FROM `2015` where content = 'F' "
while True:
	db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
	cursor = db.cursor()
	cursor.execute(sql_select)
	t = cursor.fetchall()
	print(time.asctime())
	print(len(t))

	cursor.close()
	db.close()

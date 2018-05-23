
import pymysql


for i in range(10000):
	i = i+1
	sql_update = "update `2015` set content = 'F' where id = %s"

	db = pymysql.connect('localhost', 'root', 'password', 'datetime', charset="utf8")
	cursor = db.cursor()

	cursor.execute(sql_update,i)

	db.commit()

	cursor.close()
	db.close()
	break

import pymysql
import sys


start = int(sys.argv[1])
end  = int(sys.argv[2])
db = pymysql.connect('localhost', 'root', 'password', 'datetime', charset="utf8")
cursor = db.cursor()

for i in range(start,end):
	print(i)
	sql_update = "update `2015` set content = 'F' where id = %s"

	cursor.execute(sql_update,i)

	db.commit()

cursor.close()
db.close()

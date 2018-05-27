"""
人肉多线程，每次任务开始的时候，计算有多少个待爬取的任务，根据爬虫的数目分配任务
"""
from math  import ceil
import pymysql
from multiprocessing import Pool
#from  muti_superSpider

process = 3#线程数目
thread = 8#进程数目
n = 100#每次取出的任务数目

def div(duty_list, process*2):
	sub_duty_list = []
	step = int(len(duty_list)/process)
	if len(duty_list)%process != 0:
		for i in range(process):
			sub_duty_list.append(duty_list[i*step: (i+1)*step])
		sub_duty_list[-1].extend( duty_list[process*step:])
	else:
		for i in range(process):
			sub_duty_list.append(duty_list[i*step: (i+1)*step])

	return sub_duty_list

def get_sub_duty():
	"""
	根据每次取的任务数和当前线程数目，把任务列表划分
	"""

	db = pymysql.connect('localhost', 'root', 'password', 'datetime')
	cursor = db.cursor()
	sql_select = "select * from `2015` where content = 'F' limit {}".format(n)

	cursor.execute(sql_select)
	t = cursor.fetchall()
	id_start = t[0][0]
	id_end = t[-1][0]
	duty_lenth = id_end - id_start
	duty_list = list(range(id_start, id_end+1))
	sub_duty_list = div(duty_list, process)

	cursor.close()
	db.close()

	return sub_duty_list

 
def muti(thread=thread, sub_duty):
	pass

sub_duty_list = get_sub_duty()
pool = Pool(process)

for s,name in zip(sub_duty_list,range(process)):
	pool.apply_async(muti, args(s,name))

pool.close()
pool.join()


#print(len(sub_duty_list))
#print(id_start, id_end)



# if duty_lenth < 100:
# 	#如果待爬取的任务量小于线程数目，一个线程就可以爬完
# 	pass
# else:


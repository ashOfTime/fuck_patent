from time import asctime
from multiprocessing import Pool
from muti_process_spider import muti_control
import pymysql


def div_list(ls,n):  
   result = []
   cut = int(len(ls)/n)
   if cut == 0:
       ls = [[x] for x in ls]
       none_array = [[] for i in range(0, n-len(ls))]
       return ls+none_array
   for i in range(0, n-1):
       result.append(ls[cut*i:cut*(1+i)])
   result.append(ls[cut*(n-1):len(ls)])
   return result


db = pymysql.connect('localhost', 'xwk', 'password', 'datetime')
cursor = db.cursor()
task_num =  12*1000
sql_select = "select id from `2015` where content = 'F' limit {}".format(task_num)
cursor.execute(sql_select)
task = cursor.fetchall()
task =[t[0] for t in task]
id_list = div_list(task,10)
start_time = asctime()
print('task start ',start_time)
print('the num of the task is',len(task)
)
#task_list = [[366000,367000],[367000,368000],[368000,369000],[369000,370000],[370000,371000],[371000,372000],[372000,373000],[373000,374000],[374000,375000],[375000,376000],[376000,377000]]
thread_pool = Pool(12)
thread_pool.map(muti_control, id_list)

#print('task end ',acstime())

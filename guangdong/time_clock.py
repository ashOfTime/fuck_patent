import threading
#import guangdong_num
import time

"""
这是多线程的父进程，负责调用子进程执行，并定时，时间到了无论如何，整个爬虫会被停rue止
"""
def test():
	while True:	
		print(1)

round_time = 5
t1 = threading.Thread(target=test)
t1.setDaemon(True)
t1.start()
time.sleep(round_time)#执行600s后，这个程序就会停止
print('restart {}'.format(time.asctime()))
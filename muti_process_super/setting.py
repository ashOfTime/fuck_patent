import time



process = 3#线程数目
thread = 8#进程数目
n = 7#每次取出的任务数目


"""
代理池的相关设置
"""
redis_host = 'localhost'
redis_port = 6379
min_ip =4 #代理池里最少ip数目
api = 'http://dynamic.goubanjia.com/dynamic/get/45d0e4cd0b14c3c9bcd174948ff5e969.html?sep=3&random=true'
min_cookies = 2*process#cookie池里的cookies的最小数目
min_proxys = 3 #proxy池里的proxy最小数目


# username = 'bajie123'
# password = 'bajie123'

#username = 'mie4ba4'
#password = 'mie4ba4'

username = 'bpTNn3f*_0'
password = 'bpTNn3f*_0'

#coding:utf-8
import redis
import requests
import time
from setting import redis_host,redis_port,min_ip

class ProxyPool(object):
	"""docstring for ProxyPool"""
	def __init__(self, redis_host, redis_port):
		self.Redis = redis.StrictRedis(host=redis_host, port=redis_port)
	
	def get_new_proxy(self,api):
		ip_list = requests.get(api).text.strip().split('\n')

		for ip in ip_list:
			print(ip)
			self.Redis.zadd('Proxys', time.time(), ip)

	def pop_ip(self):
		"""
		从代理池里拿出一个ip
		"""
		ip = self.Redis.zrange('Proxys',0,0, withscores=True)#把ip取出来
		self.Redis.zremrangebyrank('Proxys', 0, 0)#从队列里删除这个ip

		return ip

	def mother(self, api, min_ip, check_time=1):
		"""
		min_ip:代理池里的最少的ip的数目
		check_time:检测的时间间隔

		每隔一定时间就检测代理池里的代理数目，如果少于一定数目，就补充代理
		"""
		while True:
			ip_nums = int(self.Redis.zcard('Proxys'))
			print('the number of ip in is ',ip_nums)
			print(time.asctime())
			if ip_nums < int(min_ip):
				print('get new ip')
				self.get_new_proxy(api)
			time.sleep(check_time)

	def push_ip(self,ip,timestamp):
		"""
		ip:需要放回的ip
		timestamp:时间戳
		用完的ip放回来，连同时间戳
		"""

		self.Redis.zadd('Proxys', timestamp, ip)

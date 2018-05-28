import base64
import requests
import json
import numpy as np
import os
import shutil
import time
import os
import traceback
import time

from PIL import Image
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier

import redis
from setting import username,password

def ML_reco_valcode():
	"""
	用训练好的模型去解析验证码
	"""
	knn = joblib.load('./sipo3.job')
	image = np.asarray(Image.open('./valcode.jpg').convert('L'))
	image = (image > 135) * 255
	letters = [image[:, 6:18].reshape(20*12), image[:, 19:31].reshape(20*12), image[:, 33:45].reshape(20*12), image[:, 45:57].reshape(20*12)]

	eqution = []
	for l in letters:
		eqution.append(knn.predict(l.reshape((1,-1)))[0])
	eqution = ''.join(eqution)

	if '+' in eqution:
		split_equation = eqution.split('+')
		ans = int(split_equation[0]) + int(split_equation[1])
		ans = str(ans)

	elif '-' in eqution:
		split_equation = eqution.split('-')
		ans = int(split_equation[0]) - int(split_equation[1])
		ans = str(ans)
	else:
		#既没有加号 也没有减号，验证码识别有问题 应该重新下载 或用别的方法
		print('valcode recognize fail ')
		ans = 'False'

	print(eqution)
	print(ans)

	return eqution,ans

def get_var(s, proxies):
	"""
	获取验证码图片，保存图片和cookie到本地

	"""
	#u = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml'
	u = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'
	#u = 'http://www.baidu.com'
	headers_val = {
	    "Accept": "text / html, * / *;q = 0.01",
	    "Accept-Encoding": "gzip, deflate",
	    "Accept-Language": "zh-CN,zh;q=0.8",
	    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
	}

	flag = 0#记录获取验证码是否成功，默认失败
	rsp_val = 'F'

	try:
		rsp_val = requests.get(u, headers=headers_val, timeout=10, proxies=proxies)
		#print(rsp_val.cookies)
		if rsp_val.status_code == 200 and '访问受限' not in rsp_val.text:
			flag = 1#只有成功获取验证码，flag才会被修改成1
			#保存cookie 保存验证码图片 
			with open('valcode.jpg', 'wb') as f:
				f.write(rsp_val.content)
			requests.utils.add_dict_to_cookiejar(s.cookies,requests.utils.dict_from_cookiejar(rsp_val.cookies)) 
			#print(s.cookies)
			cookie = rsp_val.cookies
			cookie_dict = requests.utils.dict_from_cookiejar(cookie)
			cookie_json = json.dumps(cookie_dict)
			# with open('cookie.json','w') as f:
			# 	f.write(cookie_json)
			print('suss download varcode picture')

	except Exception as e:
		print('ip失效')
		print(e)
		flag = 0

	return flag

def login(s,ip):
	print('尝试登陆 {}'.format(ip))
	base64usrname = str(base64.b64encode(bytes(username,encoding='utf-8')), 'utf-8')
	base64password = str(base64.b64encode(bytes(password,encoding='utf-8')), 'utf-8')
	headers = {
    'Origin': 'http://www.pss-system.gov.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml',
    'Connection': 'keep-alive',
	}


	proxies={
	    'http':'http://{}'.format(ip),
	    'https':'https://{}'.format(ip)
	                }

    #下载验证码并保持cookies到session对象里

	flag = get_var(s, proxies)

	if flag:
		#破解验证码
		eqution,varcode_value = ML_reco_valcode()
		data = [
	  	('j_loginsuccess_url', ''),
	  	('j_validation_code', varcode_value),
	  	('j_username', base64usrname),
	  	('j_password', base64password),
			]
		#print(s.cookies)
		try:

			rsp = s.post('http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check', headers=headers, data=data, timeout=10, proxies=proxies)
			#print(rsp.text)
			if username in rsp.text:
				is_login = 1
			else:
				is_login = 0

		except:
			is_login = 0
	else:
		is_login = 0
	return is_login
	#print(s.cookies)

# s = requests.Session()
# r = redis.Redis('localhost', '6379')
# ip = r.rpop('proxys').decode('utf-8')
# print(ip)
# ip = '182.86.190.132:45067'

# ip = '49.85.5.74:26050'
# s_login = login(s,ip)
# print(is_login)
# print(s.cookies)
# print(s.get('http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml').text)
#print(s.cookies)


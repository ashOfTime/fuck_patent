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

from setting import username,password

def get_var(proxies):
	"""
	获取验证码图片，保存图片和cookie到本地。
	这里写成了一个死循环，只有网络正常且返回状态码是200才退出循环。
	后期考虑在这里加一个换代理的步骤，如果成功连接上服务器，但是没有返回值超过一定次数就换个代理。

	"""
	u = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/login-showPic.shtml'
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
		if rsp_val.status_code == 200 and '访问受限' not in rsp_val.text:
			flag = 1#只有成功获取验证码，flag才会被修改成1
			#保存cookie 保存验证码图片
			with open('valcode.jpg', 'wb') as f:
				f.write(rsp_val.content)

			cookie = rsp_val.cookies
			cookie_dict = requests.utils.dict_from_cookiejar(cookie)
			cookie_json = json.dumps(cookie_dict)
			# with open('cookie.json','w') as f:
			# 	f.write(cookie_json)
			print('suss download varcode picture')

	except Exception as e:
		print(e)
		pass

	return rsp_val,flag
	#循环检测
	#cnt_var =1#记录获取验证码图片的次数
	# for i in range(3):
	# 	print('get varcode picture......',cnt_var)
	# 	try:
	# 		rsp_val = requests.get(u, headers=headers_val, timeout=8, proxies=proxies)
	# 		if rsp_val.status_code == 200 and '访问受限' not in rsp_val.content.decode('utf-8'):
	# 			flag = 1#只有成功获取验证码，flag才会被修改成1
	# 			#保存cookie 保存验证码图片
	# 			with open('valcode.jpg', 'wb') as f:
	# 				f.write(rsp_val.content)

	# 			cookie = rsp_val.cookies
	# 			cookie_dict = requests.utils.dict_from_cookiejar(cookie)
	# 			cookie_json = json.dumps(cookie_dict)
	# 			with open('cookie.json','w') as f:
	# 				f.write(cookie_json)
	# 			print('suss download varcode picture')
	# 			break
	# 		else:
	# 			continue
	# 	except Exception as e:
	# 		print('get varcode error.......',cnt_var)
	# 		cnt_var += 1
			# print('===================================================================================')
			# traceback.print_exception()
			# print('===================================================================================')	
		#这里有一个不严禁的地方，我写这个死循环加try except是想在网络连接出现问题的的时候，不停的尝试连接。但是这个except会不会捕获到别的错误，或者还有哪些错误？

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

def get_cookies(ip,username,password):
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

	cnt_cookie = 1
	print('get login cookie ......',cnt_cookie)
	rsp_val,flag = get_var(proxies)

	status = 0
	if flag == 1:
		eqution,varcode_value = ML_reco_valcode()
		data = [
		  ('j_loginsuccess_url', ''),
		  ('j_validation_code', varcode_value),
		  ('j_username', base64usrname),
		  ('j_password', base64password),
		]
		try:
			rep_login = requests.post('http://www.pss-system.gov.cn/sipopublicsearch/wee/platform/wee_security_check', headers=headers, cookies=rsp_val.cookies, data=data, timeout=5)
			cookies = rep_login.cookies
			status = 1
		except Exception as e:
			pass

	elif flag == 0:
		print('useless ip')
		cookies = 'F'

	return cookies,status


#get_cookies('65.61.106.131:8080', username, password)


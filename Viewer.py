# ------------------------------ #
# Created by Me #
# ------------------------------ #
import requests
import threading
import sys
import os
import time
import conf
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))+"\\"
max = threading.Semaphore(value=500) # Decrease this value if you encount problems with your cpu/ram usage.
threads = []


def fetchData(channel, post, checkTimeout, proxy=None):
	try:
		r = requests.get('https://t.me/'+channel+'/'+post+'?embed=1', timeout=checkTimeout, proxies={'https':proxy})
		cookie = r.headers['set-cookie'].split(';')[0]
		key = r.text.split('data-view="')[1].split('"')[0]
		if 'stel_ssid' in cookie: 
			return {'key':key,'cookie':cookie}
		else:
			return False
	except Exception as e:
		return False

		
def addViewToPost(channel, post, checkTimeout, key=None, cookie=None, proxy=None):
	try:
		r = requests.get('https://t.me/'+channel+'/'+post+'?embed=1&view='+key, timeout=checkTimeout, headers={
		'x-requested-with':'XMLHttpRequest',
		'user-agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
		'referer':'https://t.me/'+channel+'/'+post+'?embed=1',
		'cookie':cookie}, proxies={'https':proxy}
		)
		return r.text
	except Exception as e:
		return False


def run(channel, post, proxy,checkTimeout):
	max.acquire()
	s = fetchData(channel, post, checkTimeout, 'https://'+proxy)
	if (type(s) is dict):
		l = addViewToPost(channel, post, checkTimeout, s['key'], s['cookie'], 'https://'+proxy)
	max.release()


def runThreadsWithProxies(proxies, checkTimeout, postNumber):
	maxThread = 500
	xxx = 0
	k = 0
	for proxy in proxies:
		p = proxy.split('\n')[0]
		thread = threading.Thread(target=run,args=(conf.channel,postNumber,p,checkTimeout))
		threads.append(thread)
		thread.start()
		xxx = xxx +1
		if xxx > maxThread:
			xxx = 0
			k = k + 1
			print k
			time.sleep(checkTimeout+10)

#---------------------------------------------------------
step = sys.argv[1]
with open (dir_path + str(step) + ".txt", 'r') as f:
	proxies = f.readlines()
	f.close()

runThreadsWithProxies(proxies, conf.firstTimeout, conf.postNumber)
time.sleep(conf.firstTimeout+10)

runDuration = 6300
startTime = datetime.datetime.now()
endTime = datetime.datetime.now()
while ((endTime - startTime).total_seconds()) <  runDuration : 
	for i in conf.postList:
		runThreadsWithProxies(proxies, conf.secondTimeout, i)
		time.sleep(conf.secondTimeout+10)
	endTime = datetime.datetime.now()

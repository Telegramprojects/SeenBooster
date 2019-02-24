# ------------------------------ #
# Created by Me #
# ------------------------------ #
import requests
import threading
import sys
import os
import time
import conf

dir_path = os.path.dirname(os.path.realpath(__file__))+"\\"
max = threading.Semaphore(value=500) # Decrease this value if you encount problems with your cpu/ram usage.
threads = []
mainThreads = []
step = conf.step


def mainFunc():
	# Reading last proxy
	with open(dir_path+"lastProxy.txt", 'r')  as f:
		lines = f.readlines()
		lastProxy = lines[0]
		f.close()
	print "lastProxy", lastProxy

	# Getting New Proxies from URL
	r = requests.get("https://www.proxy-list.download/api/v1/get?type=https")
	mylist = r.content
	proxies = mylist.split()
	newProxy = proxies[0]
	print "newProxy",newProxy

	# wait to get new proxies
	while newProxy == lastProxy:
		time.sleep(60)
		r = requests.get("https://www.proxy-list.download/api/v1/get?type=https")
		mylist = (r.content)
		proxies = mylist.split()
		newProxy = proxies[0]
		print len(proxies)
		print "newProxy",newProxy

	# Update last proxy
	with open(dir_path+"lastProxy.txt", 'w')  as f:
		f.write(str(newProxy))
		f.close()

	for i in range(1,step):
		with open(dir_path+str(i)+".txt",'w') as prFiles:
			# print "proxy lists created."
			for pr in range(1,len(proxies),step):
				try:
					prFiles.write(proxies[pr+i]+"\n")
				except:
					pass
		prFiles.close()

	for i in range(1,step):
		os.system("start cmd /c C:\\Python27\\python.exe "+ dir_path + "viewer.py " + str(i))


#===============================================================================
#------------------------------------Main---------------------------------------
#===============================================================================
while True:
	myThread = threading.Thread(target=mainFunc)
	mainThreads.append(myThread)
	myThread.start()
	myThread.join()
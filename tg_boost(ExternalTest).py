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

	with open(dir_path+ conf.proxyFile +".txt", 'r') as f:
		proxies = f.readlines()	

	for i in range(1,step+1):
		with open(dir_path+str(i)+".txt",'w') as prFiles:
			# print "proxy lists created."
			for pr in range(1,len(proxies),step):
				try:
					prFiles.write(proxies[pr+i]+"\n")
				except:
					pass
		prFiles.close()

	for i in range(1,step+1):
		os.system("start cmd /c C:\\Python27\\python.exe "+ dir_path + "viewer.py " + str(i))


#===============================================================================
#------------------------------------Main---------------------------------------
#===============================================================================
mainFunc()

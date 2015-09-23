#!/usr/bin/python
import xmlrpclib
import requests
import os,sys
import threading
import time

def daemonize():
  stdin = '/dev/null'
  stderr = '/dev/null'
  stdout = '/dev/null'
  try: 
  	pid = os.fork() 
  	if pid > 0:
  		# exit first parent
			sys.exit(0) 
  except OSError, e: 
  	sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
  	sys.exit(1)
  
  # decouple from parent environment
  os.chdir("/") 
  os.setsid() 
  os.umask(0) 
  
  # do second fork
  try: 
  	pid = os.fork() 
  	if pid > 0:
  		# exit from second parent
  		sys.exit(0) 
  except OSError, e: 
  	sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
  	sys.exit(1) 
  
  # redirect standard file descriptors
  sys.stdout.flush()
  sys.stderr.flush()
  si = file(stdin, 'r')
  so = file(stdout, 'a+')
  se = file(stderr, 'a+', 0)
  os.dup2(si.fileno(), sys.stdin.fileno())
  os.dup2(so.fileno(), sys.stdout.fileno())
  os.dup2(se.fileno(), sys.stderr.fileno())

def get_task():
	saeHttpServer='http://agostop.sinaapp.com/geturl'
	aria2c_rpc_url='http://192.168.0.202:6800/rpc'
	server = xmlrpclib.ServerProxy(aria2c_rpc_url)
	SLEEP_TIME = 2

	req = requests.Session()
	while True:
		downlist=[]
		opt={}
		try:
			ret = req.get(saeHttpServer)
		except :
			break
		
		try:
			if ret.text:
				ret_content = ret.text
				content = ret_content.split()
				downlist.append(content[0])
				if len(content) == 2:
					option = content[1]
					opt[ option.split('=')[0] ] = option.split('=')[1]
					aria_gid = server.aria2.addUri(downlist,opt)
					print 'have a url : %s \nthe option is : %s'%(content,opt)
				else:
					aria_gid = server.aria2.addUri(downlist)
			else:
				print 'not have task, wait...'
		except Exception,ex:
			print Exception,':',ex

		time.sleep(SLEEP_TIME)

if __name__ == '__main__':
	daemonize()
	while True:
		time.sleep(1)
		if threading.activeCount() == 1 :
			t = threading.Thread(target=get_task, name='get_task',args=())
			t.setDaemon(True)
			t.start()


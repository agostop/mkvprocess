#!/usr/bin/python
import urllib2,xmlrpclib
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


daemonize()

saeHttpServer='http://xxxxx.sinaapp.com/geturl'
aria2c_rpc_url='http://192.168.0.202:6800/rpc'
server = xmlrpclib.ServerProxy(aria2c_rpc_url)
SLEEP_TIME = 2

req = urllib2.Request(saeHttpServer)
while True:
	try:
		time.sleep(1)
		downlist=[]
		opt={}
		ret = urllib2.urlopen(req).read()
		
		if ret:
			content = ret.split()
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
		print '% : %'%(Exception,ex)

	time.sleep(SLEEP_TIME)

#!/usr/bin/python
import urllib2,xmlrpclib
import os
import time

saeHttpServer='http://xxxxxx.sinaapp.com/geturl'
aria2c_rpc_url='http://192.168.0.202:6800/rpc'
server = xmlrpclib.ServerProxy(aria2c_rpc_url)
SLEEP_TIME = 5

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

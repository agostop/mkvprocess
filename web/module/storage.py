from sae.storage import Bucket
from sae.taskqueue import Task,TaskQueue
import urllib,urllib2,time
from module import kvdb

def sfilewrite (imgurl,ftype):
	#sumtime=kvdb.qrykey('sumupload')
	#kvdb.createkey('sumupload',sumtime+1)

	#if sumtime > 30 :
	#	kvdb.replacekey('sumupload',0)

	curtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	savename='%s.%s' % (curtime,ftype)
	#Ak=kvdb.qrykey('access_token')
	f = urllib2.urlopen(imgurl)
	imgdata = f.read()
	bucket.put_object(savename,imgdata)

	#add_task('uptobce','/uploadtobce',urllib.urlencode(postdata),) 
	postdata={'objname':savename}
	queue = TaskQueue('uptobce')
	queue.add( Task ( '/uploadtobce' , urllib.urlencode(postdata) , delay=10 ) )
	#timekey=sumtime+1
	#kvdb.createkey(timekey,savename)
	return savename

def getobject (fname):
	return bucket.stat_object(fname)

bucket = Bucket('agostop')

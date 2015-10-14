from sae.storage import Bucket
import urllib2,time
from module import kvdb

def sfilewrite (imgurl,ftype):
	curtime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	savename='%s.%s' % (curtime,ftype)
	#Ak=kvdb.qrykey('access_token')
	f = urllib2.urlopen(imgurl) 
	imgdata = f.read()
	bucket.put_object(savename,imgdata)
	return 1

def getobject (fname):
	return bucket.stat_object(fname)

bucket = Bucket('agostop')

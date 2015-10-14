from module import Bce
import time,urllib2,urlparse
from sae.storage import Bucket

def help_put_image(objectname):
	return putfile(objectname,'http://bj.bcebos.com/v1/agostop/file/image/%s'%objectname,'PUT','image/jpeg')

#def help_put_video(objectname):
#	return putfile(objectname,'http://bj.bcebos.com/agostop/file/video/','PUT','')

def putfile(objectname,URL,Methon,filetype):
	#Methon = 'PUT'
	#with open(filepath) as fh:
	#mydata = open(, "rb")
	#filesize = os.path.getsize(filepath)
	mydata = bucket.get_object_contents(objectname)
	statobject = bucket.stat_object(objectname)
	filesize=statobject['bytes']

	AKEY='f4f896541b9e4083b69392c0e0d4e645'
	SKEY='b11293dfa76b43d3b73d3f324cbc5bd2'
	expSec='1800'
	lt=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(time.time()))
	Headers={'Host' : 'bj.bcebos.com',
				'Content-Length' : filesize,
				'Content-type' : filetype,
				'x-bce-date' : lt,
				}
	headers_to_sign = Headers.keys()

	u=urlparse.urlparse(URL)
	urlpath=u.path
	urlparam=urlparse.parse_qs(u.query)
	auth_string=Bce.get_SigningKey(AKEY,SKEY,lt,expSec,Methon,urlpath,urlparam,Headers,headers_to_sign)
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(URL, data=mydata)
	for k in Headers:
		request.add_header(k, Headers[k])
	request.add_header('Authorization', auth_string)
	request.get_method = lambda: Methon
	try:
		connection = opener.open(request)
	except urllib2.HTTPError,e:
		connection = e

	print 'to this line?'
	
	if connection.code == 200:
		print 'upload success'
		return 'success'
	else:
		print 'upload have a error'
		return 'upload have a error'
	#return url.code
	

bucket = Bucket('agostop')

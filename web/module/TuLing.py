#coding:utf-8
import urllib2

def ai(rec):
	mykey='981c4e54791d25d16bbaed699fdbe1c4'
	baseurl = r'http://www.tuling123.com/openapi/wechatapi?key=%s' % mykey

	return post(baseurl,rec)

def post(url, mydata):
	Methon='POST'
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	req = urllib2.Request(url,data=mydata)
	req.get_method = lambda: Methon
	response = opener.open(req)
	return response.read()

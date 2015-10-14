import hashlib,urllib2
import json
from module import kvdb

def access_auth(timestamp,nonce,signature,echostr,token = 'tongtong'):
	tmpArr = [ timestamp, nonce, token ]
	tmpArr.sort()
	tmpStr = "".join(tmpArr)
	
	tmpStr=hashlib.new("sha1", tmpStr).hexdigest() 
	
	if( tmpStr == signature ):
		return echostr
	else:
		return  'the signature is "%s" , <br> the tmpsha1 is "%s" <br>' % (signature,tmpStr)

def get_access_token(APPID,SID):
	keystr='access_token'
	url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID,SID)
	token_data = json.loads(urllib2.urlopen(url).read())
	if token_data.has_key(keystr):
		token = token_data[keystr]
		if kvdb.replacekey(keystr,token) :
			return 'ok,replace'
		kvdb.addkey(keystr,token)
		return 'ok,add'
	elif token_data.has_key('error'):
		return str(token_data)
	else:
		return 'have a error'

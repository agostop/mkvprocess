import urllib2,json
def get_access_token(APPID,SID):
	keystr='access_token'
	url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID,SID)
	token_data = json.loads(urllib2.urlopen(url).read())
	if token_data.has_key(keystr):
		token = token_data[keystr]
		return token
	elif token_data.has_key('error'):
		return str(token_data)

print get_access_token('wx214b8b79af7c3cdc','dd79754f3dae25641979109a45e7e954')

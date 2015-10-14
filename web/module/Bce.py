import hashlib,hmac
import string

def get_SigningKey(AKEY,SKEY,timestamp,exp_sec,Method,path,qryparam,Headers,headers_to_sign=None):   # "RequestStr" come from connRequest() Method
	authStringPrefix = 'bce-auth-v1/%s/%s/%s' % (
        AKEY,
        timestamp,
        exp_sec)
	
	qry = get_canonical_querystring(qryparam,True)

	header = get_headers(Headers,headers_to_sign)

	signStr='\n'.join([Method,path,qry,header])

	signingKey = HMAC_SHA256_HEX( SKEY, authStringPrefix )
	signature = HMAC_SHA256_HEX(signingKey, signStr)

	if headers_to_sign:
		result = '%s/%s/%s' % (authStringPrefix, ';'.join(headers_to_sign), signature)
	else:
		result = '%s//%s' % (authStringPrefix, signature)

	return result


def HMAC_SHA256_HEX(key,string):
	return hmac.new(key ,string , hashlib.sha256).hexdigest()


def get_canonical_querystring(params, for_signature):
	"""
	
	:param params:
	:param for_signature:
	:return:
	"""
	if params is None:
		return ''
	result = []
	for k, v in params.items():
		if not for_signature or k.lower != "Authorization".lower():
			if v is None:
				v = ''
			elif type(v) is list:
				v=v[0]
			result.append('%s=%s' % (k, normalize_string(v)))
					
	result.sort()
	return '&'.join(result)


def get_headers(headers,headers_to_sign=None):
	if headers_to_sign is None or len(headers_to_sign) == 0:
		headers_to_sign = set(["host",
													"content-md5",
													"content-length",
													"content-type"])
	result = []
	for k in headers:
		k_lower = k.strip().lower()
		value = str(headers[k]).strip()
		if k_lower.startswith('x-bce-') or k_lower in headers_to_sign:
			str_tmp = "%s:%s" % (normalize_string(k_lower), normalize_string(value))
			result.append(str_tmp)
	result.sort()

	return '\n'.join(result)


def normalize_string(in_str, encoding_slash=True):
    """
    Encode in_str.
    When encoding_slash is True, don't encode skip_chars, vice versa.

    :type in_str: string
    :param in_str: None

    :type encoding_slash: Bool
    :param encoding_slash: None
    ===============================
    :return:
        **string**
    """
    tmp = []
    for ch in convert_to_standard_string(in_str):
        if ch == '/' and not encoding_slash:
            tmp.append('/')
        else:
            tmp.append(_NORMALIZED_CHAR_LIST[ord(ch)])
    return ''.join(tmp)


def convert_to_standard_string(input_string):
    """
    Encode a string to utf-8.

    :type input_string: string
    :param input_string: None
    =======================
    :return:
        **string**
    """
    if isinstance(input_string, unicode):
        return input_string.encode('UTF-8')
    else:
        return str(input_string)


def _get_normalized_char_list():
    ret = ['%%%02X' % i for i in range(256)]
    for ch in string.ascii_letters + string.digits + '.~-_':
        ret[ord(ch)] = ch
    return ret
_NORMALIZED_CHAR_LIST = _get_normalized_char_list()

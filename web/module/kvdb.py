import sae.kvdb

def newkv():
	return sae.kvdb.Client()

def setkey(key,val):
		kv.set(key,val)

def qrykey(key):
	k = key
	val = kv.get(k)
	if val != None:
		return val
	else :
		return 0

def addkey(key,val):
	k = key
	v = val
	if kv.get(k) != None:
		return 0
	else:
		kv.add(k,v)
		return 1

def delkey(key):
	k = key
	if kv.get(key) != None:
		kv.delete(k)
		return 1
	else :
		return 0

def replacekey(key,val):
	k = key
	v = val
	if kv.get(k) != None:
		kv.replace(k,v)
		return 1
	else:
		return 0

def createkey(key,val):
	k = key
	v = val
	if kv.get(k) != None:
		if k == 'mama':
			return 0
		else:
			kv.replace(k,v)
			return 1
	else:
		kv.add(k,v)
		return 1

kv = newkv()

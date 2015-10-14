from module import kvdb

def giveanumkey(prefix,qry=0):
	key = prefix
	amount = kvdb.qrykey(key)
	
	if qry==1:
		return amount
	else:
		return 1

	if amount and amount < 10:
		amount+=1
		kvdb.replacekey(key,amount)
	else:
		amount=1
		kvdb.createkey(key,amount)
	return amount

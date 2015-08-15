#!/usr/bin/python
import chardet
import codecs

def check_contain_chinese(check_str,file_encode):
	str_sum = len(check_str)
	have_cn = 0
	cn_rate = 0

	for ch in check_str.decode(file_encode):
		if u'\u4e00' <= ch <= u'\u9fff':
			have_cn = 1
			break
	
	return have_cn

def convertEncoding(from_encode,to_encode,filepath):
	try:
		lines = open(filepath).readlines()
	except:
		print 'file open failed'
		return 0

	try :
		content = []
		f = file('%s'%filepath , 'w')
		for line in lines:
			content.append(line.decode(from_encode).encode(to_encode))

		f.writelines(content)
		f.close()
		return 1
	except:
		print 'file %s open or write failed' % filepath
		return 0

def guess_encode(data):
	file_encode='test'
	try:
		if data.decode('utf8'):
			file_encode = 'utf8'
		print 'the file is %s'%file_encode
		return file_encode
	except:
		pass

	try:
		if data.decode('gbk'):
			file_encode = 'gbk'
		print 'the file is %s'%file_encode
		return file_encode
	except:
		pass

	try:
		if data.decode('utf16'):
			file_encode = 'unicode'
		print 'the file is %s'%file_encode
		return file_encode
	except:
		return 'unknow'

def check_charset(filepath):
	try:
		f = file(filepath)
		lines = file(filepath).readlines()
		sumline = len(open(filepath).readlines())
	except:
		print 'the file open failed'
		return 0
	data = f.read()

	file_encode = guess_encode(data)

	if file_encode == 'utf8':
		cn_line = 0
		print 'check chinese:'
		for tmp in lines:
			cn_line += check_contain_chinese(tmp,file_encode)

		print 'the cn_line is %s' % cn_line
		cn_rate = float(cn_line)/sumline*100
		if int(cn_rate) > 15: # is chinese srt file ?
			print 'the rate is %s' % cn_rate
			return 1
		else:
			print 'the rate is %s\n the file is eng.' % cn_rate
			return 0

		f.close()

	elif file_encode == 'gbk':
		return convertEncoding(file_encode,'UTF-8',filepath)
	elif file_encode == 'unicode':
		print 'the file type is %s'%file_encode
		return 1
	else:
		print 'the file type is unknow'
		return 0

def test():
	filepath='en_ch.srt'
	if check_charset(filepath) == 0:
		print 'the file content is not chinese'
		pass

if __name__ == '__main__':
	test()

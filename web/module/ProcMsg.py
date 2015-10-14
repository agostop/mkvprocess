#-*- coding:utf8 -*-

from sae.taskqueue import add_task
from module import kvdb,TuLing
import xml.etree.cElementTree as ET
import time,urllib

def Process_Msg(rec):
	xml_rec = ET.fromstring(rec)

	tousr = xml_rec.find('FromUserName').text
	fmusr= xml_rec.find('ToUserName').text
	mty = xml_rec.find('MsgType').text

	if mty == 'text':
		content = xml_rec.find('Content').text
		return ProcessText(tousr,fmusr,content,rec)

	elif mty == 'image':
		url = xml_rec.find('PicUrl').text
		return ProcessImg(url,tousr,fmusr)
		#SaveImg(imgurl)

	elif mty == 'location':
		return TuLing.ai(rec)

	elif mty == 'event':
		event = xml_rec.find('Event').text
		if event == 'subscribe':
			return MsgReply(tousr,fmusr,u"欢迎来到潼潼小窝～")

	else :
		return MsgReply(tousr,fmusr,u"暂时木办法处理图片和文字之外的东东……")


def ProcessText(tou,fromu,content,rec):
	if content == u'我是妈妈':
		if kvdb.qrykey('mama') == tou : 
			if content.split()[0] == 'qr' :
				key=content.split()[1]
				if kvdb.qrykey(key):
					return MsgReply(tou,fromu,'have set %s.' % (key))
				else:
					return MsgReply(tou,fromu,'%s not set.' % (key))

			elif content.split()[0] == 'del':
				key=content.split()[1]
				if kvdb.delkey(key):
					return MsgReply(tou,fromu,'ok, already delete key . ')
				else :
					return MsgReply(tou,fromu,'can not delete ,the \'%s\' is not set .' % (key))

			return MsgReply(tou,fromu,u"妈，你来了，我知道是你～嘿嘿 ^___^ ，可以传图片啦～")

		else:
			if kvdb.addkey('mama',tou) == 1:
				return MsgReply(tou,fromu,u"喔，潼潼记住妈妈的微信号了，以后可以用这个上传图片喔。\(^o^)/")
			else :
				return MsgReply(tou,fromu,u"你是谁的妈哟～")

	else :
			#return MsgReply(tou,fromu,simai.xiaohuangji(content))
			return TuLing.ai(rec)

def MsgReply(tou,fromu,content=u"哟，哟，切克闹！"):
	#tou = xml_rec.find('tousername').text
	#fromu = xml_rec.find('FromUserName').text
	#content = xml_rec.find('Content').text
	xml_rep = "<xml>\
			<ToUserName><![CDATA[%s]]></ToUserName>\
			<FromUserName><![CDATA[%s]]></FromUserName>\
			<CreateTime>%s</CreateTime>\
			<MsgType><![CDATA[text]]></MsgType>\
			<Content><![CDATA[%s]]></Content>\
			</xml>" % (tou,fromu,str(int(time.time())),content)
	return xml_rep

def ProcessImg(url,tousr,fmusr):
	#kvdb.createkey('thisTime',time.time())
	if kvdb.qrykey('mama') == tousr:
		postdata={'url':url,'type':'jpg'}
		add_task('Tqueue','/savetostorage',urllib.urlencode(postdata)) 
		return MsgReply(tousr,fmusr,u"哔哔哔！图片接受完毕！")
	else: 
		return MsgReply(tousr,fmusr,u"潼潼看不到图片，只能和您对话了...")

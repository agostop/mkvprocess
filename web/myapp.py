#-*- coding: UTF-8 -*-
#import xml.etree.cElementTree as ET
import json
from flask import Flask, request,render_template,make_response,redirect,url_for
from module import ProcMsg,storage,uploadtobce
from module.Verify import access_auth,get_access_token
from module.ProcMsg import MsgReply
from module import kvdb


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return 'dandan'
	#return render_template('home.html')

@app.route('/dandan', methods=['GET','POST'])
def dandan():
	if request.method == 'GET':
		if not request.args :
			return 'dandan'
		return access_auth(
							request.args['timestamp'],
							request.args['nonce'],
							request.args['signature'],
							request.args['echostr']
							)

	if request.method == 'POST' :
		rec = request.data
		xml_rep=ProcMsg.Process_Msg(rec)
		response = make_response(xml_rep)
		response.content_type='application/xml'
		return response

@app.route('/baidu_webmaster_verify_55891d4ecadca60c064e5b2f993a078f.html', methods=['GET'])
def baidu_verify():
	return '55891d4ecadca60c064e5b2f993a078f'


@app.route('/savetostorage', methods=['POST'])
def uptest():
	if request.form:
		imgurl = request.form['url']
		fnameprefix = request.form['type']
		if storage.sfilewrite(imgurl, fnameprefix):
			return ''
			#return redirect(url_for('uptobce', fname=objname))
		print 'the objname is empty , the sfilewrite have a error'
		return ''
	else:
		print 'no data'
		return ''


@app.route('/uploadtobce', methods=['POST'])
def uptobce():
	if request.form:
		objname = request.form['objname']
		return uploadtobce.help_put_image(objname)
		#return objname
	else:
		print 'uploadtobce no data'
		return ''


@app.route('/failqueue',methods=['POST'])
def failqueue():
	#xml_rep=MsgReply(tou,fromu,content=u"好像粗理失败鸟……T_T")
	#response = make_response(xml_rep)
	#response.content_type='application/xml'
	
	print 'the queue is failed'
	return ''

@app.route('/getakey')
def getakey():
	return get_access_token('wx214b8b79af7c3cdc','dd79754f3dae25641979109a45e7e954')

@app.route('/getobjectinfo')
def getobjectinfo():
	if request.args:
		filename=request.args['fname']
		obj=storage.getobject(filename)
		#obj_info='\n'.join(map(str,obj))
		obj_size=obj['bytes']
		return obj_size
	print 'no data'
	return ''

@app.route('/pushurl')
def pushurl():
	try:
		MaxTask = kvdb.qrykey('maxtask')
		return render_template("offlineget.html",TASK=MaxTask)
	except Exception,ex:
		return '%s : %s'% (Exception,ex)

@app.route('/pullurl', methods=['POST'])
def pullurl():
	try:
		MaxTask = kvdb.qrykey('maxtask')
	
		if not MaxTask :
			kvdb.createkey('maxtask',0)
	
		if request.form:
			download_url = request.form['url']
			download_opt = request.form['opt']
			MaxTask += 1
			url_key = 'url_%s' % MaxTask
			url_opt = 'opt_%s' % url_key
			if not kvdb.addkey(url_key, download_url):
				kvdb.createkey(url_key,download_url)
			if not kvdb.addkey(url_opt, download_opt):
				kvdb.createkey(url_opt, download_opt)

			kvdb.setkey('maxtask',MaxTask)
			return 'now the maxtask is %s \nthe url is : %s : %s\n%s : %s' % (
					kvdb.qrykey('maxtask'),
					url_key,
					kvdb.qrykey(url_key),
					url_opt,
					kvdb.qrykey(url_opt)
					)
		else:
			return 'no form data'
	except Exception,ex:
		return '%s : %s'% (Exception,ex)

@app.route('/geturl')
def geturl():
	try:
		MaxTask = kvdb.qrykey('maxtask')
		if MaxTask == 0:
			return ''
		url = kvdb.qrykey('url_%s'%MaxTask)
		opt = kvdb.qrykey('opt_url_%s'%MaxTask)
		if not url:
			return ''
		if not kvdb.delkey('url_%s'%MaxTask):
			return 'Donot have the url_%s key'%MaxTask
		if opt:
			kvdb.delkey('opt_url_%s'%MaxTask)

		MaxTask -= 1
		kvdb.setkey('maxtask',MaxTask)
		return '%s out=%s'%(url,opt)
	except Exception,ex:
		return '%s : %s'% (Exception,ex)


if __name__ == '__main__':
	app.run(debug=True)

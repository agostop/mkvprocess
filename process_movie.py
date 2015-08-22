#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import xmlrpclib
from chdet import check_charset
from zipfile import *

DEBUG = 0

def debug_log(msg):
	if DEBUG == 1:
		print msg


def mkv_cmd(mkvfile,srtfile,finpath,origin_path):

	dir_name = os.path.dirname(mkvfile)
	_srtfile = dir_name+'/'+srtfile
	outfile = os.path.splitext(mkvfile)[0] + '.MKV_FINISHED' + os.path.splitext(mkvfile)[1]

#	mkvtool_path = '/usr/bin/avconv'
#	cmdline = '%s -i \"%s\" -i \"%s\" -c copy \"%s\"' % (mkvtool_path,mkvfile,_srtfile,outfile)
	mkvtool_path = '/usr/bin/mkvmerge'
	cmdline = '%s -o \"%s\" -S \"%s\" \"%s\"' % (mkvtool_path,outfile,mkvfile,_srtfile)
	
	print '============== the process mkv tools file is ============\n'
	print cmdline
	os.system(cmdline)
	if not os.path.exists(finpath):
		os.mkdir(finpath)
	mkv_finpath='%s/%s' % (finpath,os.path.basename(outfile))
	if os.path.exists(outfile):
		os.rename(outfile,mkv_finpath)
	debug_log('os rename %s,%s'%(outfile,mkv_finpath))
	
	origin_mkv_finpath='%s/%s' % (origin_path,os.path.basename(mkvfile))
	origin_srt_finpath='%s/%s' % (origin_path,os.path.basename(srtfile))
	os.rename(mkvfile,origin_mkv_finpath)
	os.rename(_srtfile,origin_srt_finpath)
	debug_log('os rename mkv origin %s,%s'%(mkvfile,origin_mkv_finpath))
	debug_log('os rename srt origin %s,%s'%(_srtfile,origin_srt_finpath))
	
#	srt_finpath='%s/%s' % (finpath,os.path.basename(_srtfile))
#	os.rename(mkvfile,mkv_finpath)
#	os.rename(_srtfile,srt_finpath)
#	os.system('/etc/init.d/minidlna force-reload')
#	time.sleep(5)
#	os.system('/etc/init.d/minidlna restart')

def procMovie(complist,srtlist,finpath,origin_path):
	for m in xrange(len(srtlist)):
		for n in xrange(len(complist)):
			comp_name = os.path.basename(complist[n])
			if os.path.splitext(comp_name)[0] in srtlist[m]:
				debug_log('the complist file is :%s\n\nthe srt list file is :%s'%(complist[n],srtlist[m]))
				mkv_cmd(complist[n],srtlist[m],finpath,origin_path)

def unzip(source_zip):
	srt_fname = []
	target_dir = os.path.dirname(source_zip)
	myzip = ZipFile(source_zip)
	myfilelist = myzip.namelist()
	for name in myfilelist:
		if os.path.splitext(name)[1] == '.srt':
			srt_fname.append(name)
		f_handle = open('%s/%s'%(target_dir,name),"wb")
		f_handle.write(myzip.read(name))
		f_handle.close()
	myzip.close()
	os.remove(source_zip)

	return srt_fname

def List_dir(fpath,complete_list,srtfile_list,finpath):
	other_movie_format = ['.mp4','.wmv','.rmvb','.mp3','.mpeg','.avi','.flv','.f4v']
	for filename in os.listdir(fpath):
		filepath = os.path.join(fpath, filename)
		
		if os.path.isdir(filepath):
			List_dir(filepath,complete_list,srtfile_list)
		else:
			if os.path.exists('%s%s' % (filepath,'.aria2')) or '.MKV_FINISHED.' in filepath or '.aria2' in filepath :
				print 'the continue filepath is : %s'%filepath
				continue
			debug_log(filepath)
			if os.path.splitext(filepath)[1] == '.zip':
				srtfile_list += unzip(filepath)
			elif os.path.splitext(filepath)[1] == '.mkv':
				complete_list.append(filepath)
			elif os.path.splitext(filepath)[1] in other_movie_format :
				os.rename(filepath,'%s/%s'%(finpath,os.path.basename(filepath)))
			elif os.path.splitext(filepath)[1] == '.srt':
				if not check_charset(filepath):
					print 'the srt file is process failed, maybe the file is english srt'
					os.remove(filepath)
				srtfile_list.append(os.path.basename(filepath))
				debug_log('the srtfile_list is %s' % srtfile_list)
			else:
				os.remove(filepath)
	
	return complete_list,srtfile_list

def main():
	finpath = '/home/pi/data/movie'
	origin_path = '/home/pi/data/proc_over_movie'
	comp_list=[]
	srt_list=[]
	List_dir('/home/pi/data/need_proc_movie',comp_list,srt_list,finpath)
	debug_log('the complist file is :%s\nthe srt list file is :%s' % (comp_list,srt_list))
	if len(comp_list) and len(srt_list): 
		procMovie(comp_list,srt_list,finpath,origin_path)

if __name__ == '__main__' :
	url = 'http://localhost:6800/rpc'
	server = xmlrpclib.ServerProxy(url)
	active = server.aria2.tellActive()
	if not active:
		main()
	else:
		print 'the aria2c is have a downloading'

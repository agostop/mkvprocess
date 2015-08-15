#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
from chdet import check_charset
from zipfile import *

DEBUG = 0
ENG_SRT = ['eng']

def debug_log(msg):
	if DEBUG == 1:
		print msg

def mkv_cmd(mkvfile,srtfile):
	finpath = '/home/pi/data/proc_over_movie'
	
	if not check_charset(srtfile):
		print 'the srt file is process failed, maybe the file is english srt'
		return 0

	dir_name = os.path.dirname(mkvfile)
	_srtfile = dir_name+'/'+srtfile
	outfile = os.path.splitext(mkvfile)[0] + '.new' + os.path.splitext(mkvfile)[1]

	#mkvtool_path = '/usr/bin/avconv'
	#cmdline = '%s -i \"%s\" -i \"%s\" -c copy \"%s\"' % (mkvtool_path,mkvfile,_srtfile,outfile)
	mkvtool_path = '/usr/bin/mkvmerge'
	cmdline = '%s -o \"%s\" -S \"%s\" \"%s\"' % (mkvtool_path,outfile,mkvfile,_srtfile)
	
	print '============== the process mkv tools file is ============\n'
	print cmdline
	os.system(cmdline)
	if not os.path.exists(finpath):
		os.mkdir(finpath)
	mkv_finpath='%s/%s' % (finpath,os.path.basename(mkvfile))
	srt_finpath='%s/%s' % (finpath,os.path.basename(_srtfile))
	os.rename(mkvfile,mkv_finpath)
	os.rename(_srtfile,srt_finpath)
	#os.system('/etc/init.d/minidlna force-reload')
	#time.sleep(5)
	#os.system('/etc/init.d/minidlna restart')

def procMovie(complist,srtlist):
	for m in xrange(len(srtlist)):
		for n in xrange(len(complist)):
			comp_name = os.path.basename(complist[n])
			if os.path.splitext(comp_name)[0] in srtlist[m]:
				debug_log('the complist file is :%s\n\nthe srt list file is :%s'%(complist[n],srtlist[m]))
				mkv_cmd(complist[n],srtlist[m])

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

def List_dir(fpath,complete_list,srtfile_list):
	movie_format = ['.mkv','.mp4']
	for filename in os.listdir(fpath):
		filepath = os.path.join(fpath, filename)
		
		if os.path.isdir(filepath):
			List_dir(filepath,complete_list,srtfile_list)
		else:
			if os.path.exists('%s%s' % (filepath,'.aria2')) or '.new.' in filepath:
				continue
			debug_log(filepath)
			if os.path.splitext(filepath)[1] == '.zip':
				srtfile_list += unzip(filepath)
			elif os.path.splitext(filepath)[1] in movie_format:
				complete_list.append(filepath)
				debug_log('the filepath is %s' % filepath)
			elif os.path.splitext(filepath)[1] == '.srt':
				srtfile_list.append(os.path.basename(filepath))
				debug_log('the srtfile_list is %s' % srtfile_list)
	
	return complete_list,srtfile_list

if __name__ == '__main__' :
	comp_list=[]
	srt_list=[]
	List_dir('/home/pi/data/movie',comp_list,srt_list)
	debug_log('the complist file is :%s\nthe srt list file is :%s' % (comp_list,srt_list))
	if len(comp_list) and len(srt_list): 
		procMovie(comp_list,srt_list)

#!/usr/bin/python
# -*- coding: utf-8 -*-
import time 
import os


def rm_Expired_file(filepath,Expire):
	cur_time = time.time()
	Expire_day = float(cur_time) - Expire
	to_remove=[]
	
	for dir_path,subpaths,files in os.walk(filepath):
		for f in files:
			_mtime=os.path.getmtime(os.path.join(dir_path,f))
			if _mtime < Expire_day:
				to_remove.append(os.path.join(dir_path,f))

	for f in to_remove:
		os.remove(f)

if __name__ == '__main__' :
	Expire = 60*60*24*30 # 3 month
	filepath='/home/pi/data/proc_over_movie'
	rm_Expired_file(filepath,Expire)

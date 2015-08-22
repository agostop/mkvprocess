用树莓派做了个离线下载+minidlna，
由于这个minidlna不支持外挂字幕，所以写了个脚本，在crontab里每隔一段时间扫描一次
主要功能就是把字幕整合到视频文件内，顺便还写了过滤英文字幕，转码字幕文件成utf-8编码
需要使用mkvtoolnix工具

process_movie.py 
		主要就是给mkv文件加上字幕，然后就是把其他不是mkv文件的视频文件都放在统一的文件夹下面，这个是放在crontab下，半小时跑一次，用的时候不要忘了加/usr/bin/flock -xn /tmp/test.lock -c "python xxxxx" 不然会重复执行的

minidlna_monitor.py
		用于有新文件的时候重启minidlna服务，minidlna服务里面有个inotify的配置项，但是好像不起什么作用，不知道是不是我版本太低了

rmExpire.py
		这个主要是删除一下下载文件夹里面的过期文件，我是放在crontab里面一月让跑一次的

rpc_control_aria2c.py
		这是取服务器端的下载地址的，我用的sinaapp，便宜又实惠，我觉得还行

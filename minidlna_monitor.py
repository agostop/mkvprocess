#!/usr/bin/python
from  pyinotify import  WatchManager, Notifier,ProcessEvent,EventsCodes
import os

class EventHandler(ProcessEvent): 
	def process_IN_CREATE(self, event):
		os.system('/etc/init.d/minidlna force-reload')
		os.system('/etc/init.d/minidlna restart')
		print   ("Create file: %s "  %   event.path)
#  
#     def process_IN_DELETE(self, event):
#         print  ( "Delete file: %s "  %   event.path)
#  
	def process_IN_MODIFY(self, event):
		print  ( "Modify file: %s "  %   event.path)

 
def FSMonitor(path='/home/pi/data/movie/'):
	wm = WatchManager()
	mask = EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_CREATE'] #EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_MODIFY'] |EventsCodes.FLAG_COLLECTIONS['OP_FLAGS']['IN_CREATE']
	print('mask==',mask)
	
	notifier = Notifier(wm, EventHandler())
	wm.add_watch(path, mask,rec=True)
	print( 'now starting monitor %s'%(path))
	while True:
		try:
			notifier.process_events()
			if notifier.check_events():
				notifier.read_events()
		except KeyboardInterrupt:
			notifier.stop()
			break
 
if __name__ == "__main__":
    FSMonitor()

if __name__ == '__main__':
	import time
	import systemd.daemon

	print('Starting up')
	time.sleep(10)
	print('Startup complete')
	
	systemd.daemon.notify('READY=1')
	
	while True:
		print('Hello from the Python demo service')
		time.sleep(5)

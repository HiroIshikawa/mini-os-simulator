import os


def fifo(ps):
	"""
	First-In-First-Out
	
	
	"""
	return

def purse(input):
	print(input)
	processes = []
	process = []
	for i,t in enumerate(input):
		process.append(int(t))
		print('current process: '+str(process))
		if i!=0 and i%2 != 0: 
			t_process = tuple(process)
			processes.append(t_process)
			print('current processes: ' + str(processes))
			process[:] = []
	print(process)
	print(processes)
	fifo_result = fifo(processes)
	# 
	# report(fifo_result)
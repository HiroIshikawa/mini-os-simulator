import os


def fifo(ps):
	"""
	First-In-First-Out
	
	Run processes in order of arrivals.
	"""
	accm_time = 0
	turn_arounds = []
	# sort based on arrival time
	ps = sorted(ps, key=lambda x: x[0])
	# naive approach, not order invariant
	for p in ps:
		accm_time = accm_time + p[1]
		ta = accm_time - p[0]
		turn_arounds.append(ta)
	return turn_arounds

def schedule(ps):
	"""Apply each scheduling algos."""
	scheduleds = []
	scheduleds.append(fifo(ps))
	# results.append(sjf(ps))
	# results.append(srt(ps))
	# results.append(mlf(ps))
	return scheduleds

def purse(input):
	# print(input)
	processes = []
	process = []
	for i,t in enumerate(input):
		process.append(int(t))
		# print('current process: '+str(process))
		if i!=0 and i%2 != 0: 
			t_process = tuple(process)
			processes.append(t_process)
			# print('current processes: ' + str(processes))
			process[:] = []
	# print(process)
	# print(processes)
	# fifo_result = fifo(processes)
	# print(fifo_result)
	# 
	# report(fifo_result)
	return processes
import os

class Process:
	def __init__(self,pid,at,pt):
		self.pid = pid
		self.arrival_t = at
		self.processing_t = pt
		self.remaining_t = self.processing_t
		self.waiting_t = 0
		self.turnaround_t = 0

	def run(self):
		self.remaining_t = self.remaining_t - 1

	def wait(self):
		self.waiting_t = self.waiting_t + 1

	def turnaround(self):
		self.turnaround_t = self.processing_t + self.waiting_t


def clean_turnarounds(tas):
	results = []
	tas = sorted(tas, key=lambda x: x[0])
	for ta in tas:
		results.append(ta[1])
	return results

def fifo(ps):
	"""
	First-In-First-Out
	
	Run processes in order of arrivals.
	"""
	# accm_time = 0
	# turn_arounds = []
	# # sort based on arrival time
	# ps = sorted(ps, key=lambda x: x[1][0])
	# # naive approach, not order invariant
	# for p in ps:
	# 	accm_time = accm_time + p[1][1]
	# 	ta = accm_time - p[1][0]
	# 	pid = p[0]
	# 	pid_ta = (pid, ta)
	# 	turn_arounds.append(pid_ta)
	# # sort the turn arounds based on the priginal pid
	# turn_arounds = clean_turnarounds(turn_arounds)
	return turn_arounds

def sjf(ps):
	"""
	Shortest-Job-First

	Process with shorter running time runs first.
	"""
	accm_time = 0
	turn_arounds = []
	print(ps)
	# for p in ps:
	# 	accm_time = accm_time + p[1]
	# 	ta = accm_time - p[0]
	# 	turn_arounds.append(ta)
	return turn_arounds

def schedule(ps):
	"""Apply each scheduling algos."""
	scheduleds = []
	print(ps)
	# scheduleds.append(fifo(ps))
	# scheduleds.append(sjf(ps))
	# results.append(srt(ps))
	# results.append(mlf(ps))
	return scheduleds

def purse(input):
	"""
	Purse the input.

	Input has no syntax/semantics error in it.
	Thus, no need of error handling for input.
	"""
	# # print(input)
	# processes = []
	# process = []
	# for i,t in enumerate(input):
	# 	process.append(int(t))
	# 	# print('current process: '+str(process))
	# 	if i!=0 and i%2 != 0: 
	# 		t_process = tuple(process)
	# 		processes.append(t_process)
	# 		# print('current processes: ' + str(processes))
	# 		process[:] = []
	# id_process_s = []
	# for i,p in enumerate(processes):
	# 	id_process = (i, processes[i])
	# 	id_process_s.append(id_process)
	# return id_process_s
	processes = []
	for i in range(len(input)):
		if i%2 != 0:
			pid = i/2
			p = Process(pid,input[0],input[1])
			processes.append(p)
	return processes

def report(f, tas):
	# for each turn arounds
	for ta in tas:
		T = sum(ta) / (len(ta) * 1.0)
		# T = round(T, 2)
		T = format(T, '.2f')
		# f.write(str(T))
		f.write(T)
		f.write(' ')
		for r in ta:
			f.write(str(r))
			f.write(' ')
		f.write('\n')
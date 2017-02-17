import os

class Process:
	"""
	Process in self-time management strategy.

	Attributes:
		pid: process id
		arrival_t: arrival time, constant
		processing_t: processing time, constant
		remaining_t: remaining time
		waiting_t: waiting time
		turnaround_t: turn-around time
	"""
	def __init__(self,pid,at,pt):
		"""Initiate a process"""
		self.pid = pid
		self.arrival_t = at
		self.processing_t = pt
		self.remaining_t = self.processing_t
		self.waiting_t = 0
		self.turnaround_t = 0

	def run(self):
		"""Run this process with a unit of time slice"""
		self.remaining_t = self.remaining_t - 1

	def wait(self):
		"""Count up waiting time with a unit of time slice"""
		self.waiting_t = self.waiting_t + 1

	def turnaround(self):
		"""Compute the turn aroudn of time of this process"""
		self.turnaround_t = self.processing_t + self.waiting_t

class Scheduler:
	"""
	Base class of scheduling algorims. 

	Attributes:
		time_elapsed: the time passed by
		running_process: currently running process
		waiting_ps: list of waiting processes
		remaining_ps: list of remaining processes
	"""
	def __init__(self, ps):
		self.time_elapsed = 0
		self.running_p = None
		self.waiting_ps = []
		self.remaining_ps = ps
		self.complete_ps = []

	def elapse(self):			
		self.time_elapsed = self.time_elapsed + 1

	def schedule(self):
		# stopper = 0
		while(self.remaining_ps or self.waiting_ps or self.running_p):
			self.elapse()
			print(self.running_p)
			print(self.waiting_ps)
			print(self.remaining_ps)
			print('')
			# if stopper > 10:
			# 	break
			# else:
			# 	stopper = stopper + 1

	def report(self):
		self.schedule()
		results = []
		if self.complete_ps:
			ps = sorted(self.complete_ps, key=lambda x: x.pid)
		for p in ps:
			results.append(p.turnaround_t)
		return results


class Fifo(Scheduler):
	"""
	FIFO scheduling algorithm.
	"""

	def elapse(self):
		# if there's any finished process, calc turnaround time
		if self.running_p:
			if self.running_p.remaining_t == 0:
				self.running_p.turnaround()
				self.complete_ps.append(self.running_p)
				self.running_p = None
		# search arriving processes
		# arriving_ps = []
		removing_ix = 0
		# print('len: '+str(len(self.remaining_ps)))
		# for p in self.remaining_ps:
		# 	print('p: '+str(p))
		# 	print('p.arrival_t: '+str(p.arrival_t))
		# 	print('self.time_elapsed: '+str(self.time_elapsed))
		# 	if p.arrival_t == self.time_elapsed:
		# 		arriving_ps.append(p)
		# 		self.remaining_ps.pop(removing_ix)
		# 		removing_ix = removing_ix + 1
		# 	else:
		# 		removing_ix = removing_ix + 1
		for i in range(len(self.remaining_ps)):
			# print('p: '+str(self.remaining_ps[removing_ix]))
			# print('arrival_t: '+str(self.remaining_ps[removing_ix].arrival_t))
			# print('self.time_elapsed: '+str(self.time_elapsed))
			if self.remaining_ps[removing_ix].arrival_t == self.time_elapsed:
				# arriving_ps.append(self.remaining_ps[removing_ix])
				self.waiting_ps.append(self.remaining_ps[removing_ix])
				self.remaining_ps.pop(removing_ix)
			else:
				removing_ix = removing_ix + 1


		# presumably the coming order is the arriving time
		# if arriving_ps:
		if not self.running_p and self.waiting_ps:
			self.running_p = self.waiting_ps.pop(0)
			# for waiting_p in arriving_ps:
			# 	self.waiting_ps.append(arriving_p)
		
		# elapse all the running, waiting proess
		if self.running_p:
			self.running_p.run()
		for waiting_p in self.waiting_ps:
			waiting_p.wait()

		# elapse scheduler
		self.time_elapsed = self.time_elapsed + 1

		

def clean_turnarounds(tas):
	results = []
	tas = sorted(tas, key=lambda x: x[0])
	for ta in tas:
		results.append(ta[1])
	return results

# def fifo(ps):
# 	"""
# 	First-In-First-Out
	
# 	Run processes in order of arrivals.
# 	"""
# 	# accm_time = 0
# 	# turn_arounds = []
# 	# # sort based on arrival time
# 	# ps = sorted(ps, key=lambda x: x[1][0])
# 	# # naive approach, not order invariant
# 	# for p in ps:
# 	# 	accm_time = accm_time + p[1][1]
# 	# 	ta = accm_time - p[1][0]
# 	# 	pid = p[0]
# 	# 	pid_ta = (pid, ta)
# 	# 	turn_arounds.append(pid_ta)
# 	# # sort the turn arounds based on the priginal pid
# 	# turn_arounds = clean_turnarounds(turn_arounds)
# 	return turn_arounds

# def sjf(ps):
# 	"""
# 	Shortest-Job-First

# 	Process with shorter running time runs first.
# 	"""
# 	accm_time = 0
# 	turn_arounds = []
# 	print(ps)
# 	# for p in ps:
# 	# 	accm_time = accm_time + p[1]
# 	# 	ta = accm_time - p[0]
# 	# 	turn_arounds.append(ta)
# 	return turn_arounds

def schedule(ps):
	"""Apply each scheduling algos."""
	scheduleds = []
	print(ps)
	for p in ps:
		print(p.arrival_t)
	fifo = Fifo(ps)
	scheduleds.append(fifo.report())
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
			p = Process(pid,int(input[i-1]),int(input[i]))
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
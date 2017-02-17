import os

import copy

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

	# def elapse(self):			
	# 	self.time_elapsed = self.time_elapsed + 1

	def check_exit(self):
		# if there's any finished process, calc turnaround time
		if self.running_p:
			if self.running_p.remaining_t == 0:
				self.running_p.turnaround()
				self.complete_ps.append(self.running_p)
				self.running_p = None

	def check_entry(self):
		removing_ix = 0
		for i in range(len(self.remaining_ps)):
			if self.remaining_ps[removing_ix].arrival_t == self.time_elapsed:
				self.waiting_ps.append(self.remaining_ps[removing_ix])
				self.remaining_ps.pop(removing_ix)
			else:
				removing_ix = removing_ix + 1

	def elapse(self):
		# elapse all the running, waiting proess
		if self.running_p:
			self.running_p.run()
		for waiting_p in self.waiting_ps:
			waiting_p.wait()
		# elapse scheduler
		self.time_elapsed = self.time_elapsed + 1		

	def schedule(self):
		# stopper = 0
		while(self.remaining_ps or self.waiting_ps or self.running_p):
			# self.elapse()
			self.proceed()

	def report(self):
		self.schedule()
		results = []
		if self.complete_ps:
			ps = sorted(self.complete_ps, key=lambda x: x.pid)
		for p in ps:
			results.append(p.turnaround_t)
		return results


class Fifo(Scheduler):
	"""FIFO scheduling algorithm."""

	def proceed(self):
		self.check_exit()
		self.check_entry()
		# presumably the coming order is the arriving time
		if not self.running_p and self.waiting_ps:
			self.running_p = self.waiting_ps.pop(0)
		self.elapse()


class Sjf(Scheduler):
	"""Shortest-Job-First"""

	def proceed(self):
		self.check_exit()
		self.check_entry()
		# presumably the coming order is the arriving time
		if not self.running_p and self.waiting_ps:
			self.waiting_ps = sorted(self.waiting_ps, key=lambda x: x.remaining_t)
			self.running_p = self.waiting_ps.pop(0)
		self.elapse()


def schedule(ps):
	"""Apply each scheduling algos."""
	scheduleds = []
	fifo = Fifo(copy.deepcopy(ps))
	scheduleds.append(fifo.report())
	sjf = Sjf(copy.deepcopy(ps))
	scheduleds.append(sjf.report())
	# results.append(srt(ps))
	# results.append(mlf(ps))
	return scheduleds

def purse(input):
	"""
	Purse the input.

	Input has no syntax/semantics error in it.
	Thus, no need of error handling for input.
	"""
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
		T = format(T, '.2f')
		f.write(T)
		f.write(' ')
		for r in ta:
			f.write(str(r))
			f.write(' ')
		f.write('\n')
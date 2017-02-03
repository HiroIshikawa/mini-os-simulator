import sys
from collections import deque


class ListLayer:
	"""
	Manage order of processes in different priority

	Attributes:
		priority: 0 (init), 1 (user), or 2 (system)
		list: processes
		listLength: number of processses
	"""
	def __init__(self, priority):
		"""Initiate layer with priority"""
		self.priority = priority
		self.list = deque()  # deque works well for timeout
		self.listLength = len(self.list)  # used for stats

	def insert(self, p):
		"""Add new PCB at the end of the queue of this layer"""
		self.list.append(p)

	def remove(self):
		"""Replace the head of the queue to the next PCB and
		put the head to the end of the queue
		"""
		p = self.list.popleft()  # pop the head
		self.list.append(p)  # put the head at the end
		q = self.list[0]  # take the new head PCB
		q.status.type == 'ready'  # change the type of new PCB to 'ready'

	def check(self):
		print('---List Layer---')
		print('Priority: '+ str(self.priority))
		# print(self.list)
		for i in self.list:
			i.check()
		print('-List Layer END-')
		# print(self.listLength)


class ListStack:
	"""
	Manage order of processes in different priority

	Attributes:
		priority: 0 (init), 1 (user), or 2 (system)
		list: processes
		listLength: number of processses
	"""
	def __init__(self):
		"""Initiate a stack of lists for each priority levels"""
		self.init = ListLayer(0)
		self.user = ListLayer(1)
		self.system = ListLayer(2)

	def check(self):
		print('----List Stack----')
		self.init.check()
		self.user.check()
		self.system.check()
		print('--List Stack END--')


class RCB:
	"""
	Represents resource control block

	Attributes:
		rid: the name of resource
		status: the status of RCB, initial units and available units
		waitingList: list of blocked processes
	"""
	class Status:
		"""
		Represents RCB status

		Attributes:
			k: initial available units (fixed)
			u: available units (variable)
		"""
		def __init__(self, k, u):
			self.k = k
			self.u = u

		def check(self):
			print('Capacity: '+str(self.k))
			print('Available: '+str(self.u))

	def __init__(self, rid, k, u):
		self.rid = rid
		self.status = self.Status(k,u)
		self.waitingList = ListStack()

	def check():
		print('RID: '+str(self.rid))
		self.status.check()
		self.waitingList.check()


class ResourceStack:
	"""
	Represents the set of RCBs used in the session.


	"""
	def __init__(self):
		self.r1 = RCB('R1',1,1)
		self.r2 = RCB('R2',2,2)
		self.r3 = RCB('R3',3,3)
		self.r4 = RCB('R4',4,4)

	def check():
		self.r1.check()
		self.r2.check()
		self.r3.check()
		self.r4.check()

class PCB:
	"""
	Process Control Block

	Attributes:
		pid: name of the process
		otherResources: points to a resources control block when request happens
		status: represents the current status of the process
		crTree: pointing to parent PCB and Chlid PCB
		priority: 0, 1, or 2
	"""
	class Status:
		"""
		Represents PCB status

		Attributes:
			type: running, ready, or blocked
			list: backpointer to either ReadyList or WaitingList
		"""
		def __init__(self):
			self.type = None
			self.list = None

		# def __init__(self, type, list):
		# 	self.type = type
		# 	self.list = list

		def check(self):
			print('Type: '+str(self.type))
			print('List: '+str(self.list))

	def __init__(self, pid, priority):
		self.pid = pid
		self.otherResources = deque()
		self.status = self.Status()
		# self.crTree = CreationTree()
		self.parent = None
		self.chlid = None
		self.priority = priority

	def check(self):
		print('---PCB---')
		print('PID: '+self.pid)
		print('Resources: '+str(self.otherResources))
		self.status.check()
		print('Parent: '+str(self.parent))
		print('Child: '+str(self.parent))
		print('Priority: '+str(self.priority))
		print('-PCB END-')


class CreationTree:
	"""
	Represents the order of creation of processes

	Attributes:
		root: root of creation tree
	"""
	def __init__(self):
		self.root = deque()

	def add(self, p):
		"""Add nwe porcess to creatino tree"""
		self.root.append(p)

	def check(self):
		print('------CRT------')
		for i in self.root:
			i.check()
		print('----CRT END----')


class Manager:
	"""
	Manage entire processes and resource management.

	Attributes:
		RL: ready list
		crTree: root of CreationTree
		RS: resource stack
	"""
	def __init__(self):
		p = PCB('init',0)
		p.status.type = 'ready' 
		self.RL = ListStack()
		p.status.list = self.RL
		self.crTree = CreationTree()
		self.crTree.add(p)
		self.RL.init.insert(p)
		self.RS = ResourceStack()
		self.scheduler(p)

	def find_highest_priority(self):
		"""Find the PCB with highest prioirity"""
		if self.RL.system.list:
			return self.RL.system.list[0]
		elif self.RL.user.list:
			return self.RL.user.list[0]
		else:
			return self.RL.init.list[0]

	def preemp(self, q, p):
		"""Swap the state of two processes"""
		p.status.type = 'ready'    # make currently running processs to be ready
		q.status.type = 'running'  # make currently ready process to be running

	def scheduler(self, p):
		"""Execute policy everytime command happend"""
		q = self.find_highest_priority()
		print('exsting highest priority: '+str(q.priority)+' '+str(q.pid)+' '+str(q.status.type))
		print('new process priority: '+str(p.priority)+' '+str(p.pid)+' '+str(p.status.type))
		if (int(p.priority) < int(q.priority) or  # called from create or release
			p.status.type != 'running' or  		  # called from request or timeout
			p == None):							  # called from destroy
			self.preemp(q, p)
			print('Preempted, Process '+q.pid+' is running')
		else:
			print('Keep it, Process '+p.pid+' is running')

	def create(self, name, priority):
		"""
		Create new process.

		Status: (none) -> Ready
		"""
		# create PCB data struct / initialize PCB using params
		p = PCB(name, priority)  # create new PCB with given pid and priority
		p.status.type = 'ready'  # set status type 'ready' as default
		if priority=='1':
			self.RL.user.insert(p)
		else:
			self.RL.system.insert(p)
		p.status.list = self.RL
		self.crTree.add(p)
		self.scheduler(p)

	def request(self, rid, units):
		if rid=='R1':
			r = self.RS.r1
		elif rid=='R2':
			r = self.RS.r2
		elif rid=='R3':
			r = self.RS.r3
		else:
			r = self.RS.r4
		p = self.find_highest_priority()  # fetch currently running process
		if r.status.u >= int(units):  # if units are availble for the requiesting resource
			print("Availble!!")
			r.status.u = r.status.u - int(units)  # subtract requested units from available units
			p.otherResources.append(r)  # append the RCB to other resources in the runnnig PCB
			self.scheduler(p)
		else:
			p.status.type = 'blocked'
			p.status.list = r
			if p.priority=='2':
				self.RL.system.remove()
				r.waitingList.system.insert(p)
				q = self.RL.system.list[0]
				self.scheduler(q)
			elif p.priority=='1':
				self.RL.user.remove()
				r.waitingList.user.insert(p)
				q = self.RL.user.list[0]
				self.scheduler(q)
			else:
				print('Req, this is the p: '+p.priority)
				print('Req No process running')

	def timeout(self):
		"""
		Invoke context switch.
		"""
		p = self.find_highest_priority()  # finding running process
		if p.priority=='2':
			self.RL.system.remove()
			q = self.RL.system.list[0]
			self.scheduler(q)
		elif p.priority=='1':
			self.RL.user.remove()
			q = self.RL.user.list[0]
			self.scheduler(q)
		else:
			print('To, this is the p: '+p.priority)
			print('No process running')
		
	def check(self):
		print('---------Manager----------')
		self.RL.check()
		self.crTree.check()
		print('--------Manager END-------')


def destroy():
	pass

def initialize():
	# destroy everything

	# make ready list wiht priority 0, 1, 2
	readyList = ListStack()
	readyList.check()
	# create a single process with proprity 0
	# initiate process
	create('init',0)
	# add this to ready list 0

	# initiate 4 resources R1, R2, R3, R4
	# initiate an IO resource
	pass

def release():
	pass

def timeout():
	pass

def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def parse(manager, input):
	# check basic command error
	# checking type
	if not isinstance(input, str):
		return
	# remove leading/ending whitespaces
	input.strip()
	# count number of args
	args = input.split()
	if not args:
		return 'no input'
	# command
	if args[0]=='init':
		if (len(args) >= 2):
			return 'init: no argument allowed'
		initialize()
	elif args[0]=='cr':
		if len(args) <= 2:
			return 'create: need two arguments, name and priority'
		if len(args) >= 4:
			return 'create: too many arguments'
		if is_int(args[1]):
			return 'create: name should be one char'
		if len(args[1]) >= 2:
			return 'create: name should be one char'
		if not is_int(args[2]):
			return 'create: priority should be integer'
		if (int(args[2]) <= 0 or int(args[2]) >= 3):
			return 'create: priority should be 1 or 2'
		manager.create(args[1], args[2])  # pid, priority
	elif args[0]=='de':
		if len(args) <= 1:
			return 'destroy: need one argument, name'
		if len(args) >= 3:
			return 'destroy: too many arguments'
		if is_int(args[1]):
			return 'destroy: integer, name should be one char'
		if len(args[1]) >= 2:
			return 'destroy: too many chars, name should be one char'
		destroy()
	elif args[0]=='req':
		if len(args) <= 2:
			return 'reqeust: need two arguments, name and priority'
		if len(args) >= 4:
			return 'reqeust: too many arguments'
		if is_int(args[1]):
			return 'reqeust: integer, resource name should be two char'
		if len(args[1]) >= 3:
			return 'reqeust: too many chars, resource name should be two char'
		if len(args[1]) <= 1:
			return 'reqeust: too less char, resource name should be two char'
		if args[1][0] != 'R':
			return 'request: resource name, should be labeled with R'
		if not is_int(args[1][1]):
			return 'request: resource name, should be R1,R2,R3,or R4'
		if int(args[1][1]) <= 0 or int(args[1][1]) >= 5:
		 	return 'request: resource name, should be R1,R2,R3,or R4'
		if not is_int(args[2]):
			return 'reqeust: unit should be integer'
		if int(args[2]) <= 0 or int(args[2]) >= 3:
			return 'reqeust: unit should be 1,2,3 or 4'
		if int(args[1][1]) == 1:
			if int(args[2]) != 1:
		 		return 'request: R1 can take only 1 unit to request'
		if int(args[1][1]) == 2:
			if int(args[2]) >= 3:
		 		return 'request: R2 can take only 2 unit max to request'
		if int(args[1][1]) == 3:
			if int(args[2]) >= 4:
		 		return 'request: R3 can take only 3 unit max to request'
		if int(args[1][1]) == 4:
			if int(args[2]) >= 5:
		 		return 'request: R4 can take only 4 unit max to request'
		manager.request(args[1], args[2])  # rid, units
	elif args[0]=='rel':
		if len(args) <= 2:
			return 'release: need two arguments, name and priority'
		if len(args) >= 4:
			return 'release: too many arguments'
		if is_int(args[1]):
			return 'release: integer, resource name should be two char'
		if len(args[1]) >= 3:
			return 'release: too many chars, resource name should be two char'
		if len(args[1]) <= 1:
			return 'release: too less char, resource name should be two char'
		if args[1][0] != 'R':
			return 'release: resource name, should be labeled with R'
		if not is_int(args[1][1]):
			return 'release: resource name, should be R1,R2,R3,or R4'
		if int(args[1][1]) <= 0 or int(args[1][1]) >= 5:
		 	return 'release: resource name, should be R1,R2,R3,or R4'
		if not is_int(args[2]):
			return 'release: unit should be integer'
		if int(args[2]) <= 0 or int(args[2]) >= 3:
			return 'release: unit should be 1,2,3,or4'
		release()
	elif args[0]=='to':
		if len(args) >= 2:
			return 'time-out: no argument allowed'
		manager.timeout()
	else:
		return 'available commands: init, cr <name> <priority>, de <name>, req <resource name> <unit>, rel <resource name> <unit>, to'

	# argument
	parsed_input = input
	return parsed_input

def initiate():
	manager = Manager()
	# manager.check()
	while(1):
		var = raw_input()
		res = parse(manager, var)
		# print(res)
		# manager.check()

def call(input):
	# parse
	res = parse(input)
	return res

def display(res):
	print(res)

def driver(input):	
	# wait user's input
	# print(type(var))
	# call process / resource manager and receive response
	response = call(input)
	# display output
	display(response)
	# display()

def shell():
	while(1):
		var = raw_input()
		driver(var)
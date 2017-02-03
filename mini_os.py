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
		self.priority = priority
		self.list = deque()
		self.listLength = len(self.list)

	def insert(self, p):
		self.list.append(p)

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
			print(self.k)
			print(self.u)

	def __init__(self, rid, k, u):
		self.rid = rid
		self.status = self.Status(k,u)
		self.waitingList = ListStack()


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
		self.otherResources = None
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
	"""
	def __init__(self):
		p = PCB('init',0)
		self.RL = ListStack()
		self.crTree = CreationTree()
		self.crTree.add(p)
		self.RL.init.insert(p)

	def check(self):
		print('---------Manager----------')
		self.RL.check()
		self.crTree.check()
		print('--------Manager END-------')


def create(name, priority):
	"""
	Create new process.

	Status: (none) -> Ready
	"""
	# create PCB data struct / initialize PCB using params
	pcb = PCB(name, priority)
 #    link PCB to creation tree
 #    insert(RL, PCB)
 #    scheduler()
	pass

def destroy():
	pass

def scheduler():
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

def request():
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

def parse(input):
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
		create()
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
		request()
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
		timeout()
	else:
		return 'available commands: init, cr <name> <priority>, de <name>, req <resource name> <unit>, rel <resource name> <unit>, to'

	# argument
	parsed_input = input
	return parsed_input

def initiate():
	manager = Manager()
	manager.check()

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
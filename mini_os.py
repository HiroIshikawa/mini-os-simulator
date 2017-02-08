import sys
from collections import deque


"""
Errro handlings:
- if you try to destroy a process that hasn't been created
- if you try to release a resource that hasn't been requested

"""

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

	def rotate(self):
		"""Replace the head of the queue to the next PCB and
		put the head to the end of the queue
		"""
		p = self.list.rotate(-1)
		# p = self.list.popleft()  # pop the head
		# self.list.append(p)  # put the head at the end
		q = self.list[0]  # take the new head PCB
		q.status.type == 'ready'  # change the type of new PCB to 'ready'

	def remove(self, p):
		"""Remove particular PCB with destroy
		"""
		for i,pcb in enumerate(self.list):
			# print('Removing, current list contents: '+str(len(self.list)))
			if p.pid == pcb.pid:
				listed_queue = list(self.list)
				# print('popping: '+p.pid)
				listed_queue.pop(i)
				# self.list.clear()
				self.list = deque(listed_queue)

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
		# self.waitingList = ListStack()
		self.waitingList = []

	def check():
		print('RID: '+str(self.rid))
		self.status.check()
		# self.waitingList.check()
		print('waiting list: ')
		for p in waitingList:
			p.check()


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


	class CreationTree:
		"""
		Represents the order of creation of processes

		Attributes:
			parent: parent PCB
			children: children PCB
		"""
		def __init__(self):
			self.parent = None
			self.children = deque()

		def check(self):
			print('Parent: '+self.parent.check())
			print('Children: ')
			for child in self.children:
				child.check()

	def __init__(self, pid, priority):
		self.pid = pid
		self.otherResources = deque()
		self.status = self.Status()
		# self.crTree = CreationTree()
		# self.parent = None
		# self.child = None
		self.crTree = self.CreationTree()
		self.priority = priority

	def check(self):
		print('---PCB---')
		print('PID: '+self.pid)
		print('Resources: '+str(self.otherResources))
		self.status.check()
		self.crTree.check()
		print('Priority: '+str(self.priority))
		print('-PCB END-')



class Resource:
	"""
	Represents resource unit in other resources in PCB

	Attributes:
		rcb: RCB
		unit: consumed resource
	"""
	def __init__(self, r, units):
		self.r = r
		self.units = units


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
		p.crTree.parent = None
		self.RL = ListStack()
		p.status.list = self.RL
		# self.crTree = CreationTree()
		# self.crTree.add(p)
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
		# print('exsting highest priority: '+str(q.priority)+' '+str(q.pid)+' '+str(q.status.type))
		# print('new process priority: '+str(p.priority)+' '+str(p.pid)+' '+str(p.status.type))
		if (int(p.priority) < int(q.priority) or  # called from create or release
			p.status.type != 'running' or  		  # called from request or timeout
			p == None):							  # called from destroy
			self.preemp(q, p)
			# print('Preempted, Process '+q.pid+' is running')
			# print(q.pid)
		else:
			# print('Keep it, Process '+p.pid+' is running')
			# print(p.pid)
			pass

	def init(self):
		p = self.RL.init.list[0]  # find the init
		if p.crTree.children:
			for child in p.crTree.children:
				self.kill_tree(child)  # destroy all the process under the init
			# self.kill_tree(p)
		else:
			# print('No process exists')
			# return 'No process exests'
			pass

		# except IndexError:
		# 	print('No process exists')
		# 	return 'No process exests'
		# 	pass

	def create(self, name, priority):
		"""
		Create new process.

		Status: (none) -> Ready
		"""
		# conduct the search first to prevent duplicates name
		init = self.RL.init.list[0]
		if self.tree_search(init, name):
			# print('No duplicates in process names allowed.')
			p = self.find_highest_priority()
			self.scheduler(p)
			return 'No duplicates in process names allowed.'
		# create PCB data struct / initialize PCB using params
		p = PCB(name, priority)  # create new PCB with given pid and priority
		p.status.type = 'ready'  # set status type 'ready' as default
		# establish link between currently running process and this new process
		q = self.find_highest_priority()
		# print('Appending '+p.pid+' to '+q.pid)
		q.crTree.children.append(p)
		# print('child: '+q.crTree.children[0].pid)
		p.crTree.parent = q
		# print('parent: '+p.crTree.parent.pid)
		if priority=='1':
			self.RL.user.insert(p)
		else:
			self.RL.system.insert(p)
		p.status.list = self.RL
		self.scheduler(p)

	def kill_tree(self, p):
		"""
		Kill the all child processses of the given process.
		"""
		if p:
			# print('yes there is...')
			for child in p.crTree.children:
				self.kill_tree(child)
			pri = p.priority
			for resource in p.otherResources:
				self.release(resource.r.rid, resource.units, False)
			p.otherResources.clear()
			# print('deleting..: '+p.pid)
			parent = p.crTree.parent
			for i, child in enumerate(parent.crTree.children):
				if p.pid == child.pid:
					listed_children = list(parent.crTree.children)
					# print('popping: '+p.pid)
					listed_children.pop(i)
					# self.list.clear()
					parent.crTree.children = deque(listed_children)
					# print('Depoint '+p.pid+' from '+parent.pid)
			rl = p.status.list  # delet from the RL
			if not isinstance(rl, list):
				if pri == '2':
					rl.system.remove(p)
				elif pri == '1':
					rl.user.remove(p)
				else:
					# print('No process to remove from ready list')
					pass
			else:
				for i,pcb_units in enumerate(rl):
					if p.pid == pcb_units[0].pid:
						rl.pop(i)
			p = None
			return
		return

	def tree_search(self, tree, name):
		"""
		Search an element.
		"""
		result = None
		# if not tree.crTree.children:
		# 	print('Theres no children')
		# 	return
		# for child in tree.crTree.children:
		# 	if child.pid == name:
		# 		print('Target found: '+child.pid)
		# 		return child
		# 	else:
		# 		result = self.tree_search(child, name)
		if tree.pid == name:
			# print('Target found: '+tree.pid)
			return tree
		else:
			for child in tree.crTree.children:
				result = self.tree_search(child, name)
				if result:
					break
		return result

	def destroy(self, name):
		"""
		Destroy the process, name.

		Status: Running/Ready/Blocked -> (None)
		Restricted to apply this to the descendants of
		currently running process or the process itself
		"""
		# root = self.RL.init.list[0]  # init process
		p = self.find_highest_priority()  # the running process
		# print('root: '+root.pid)
		# print('currently running: '+p.pid)
		# start search from root
		# target = self.tree_search(root, name)
	# if name == p.pid:
	# 	self.kill_tree(p)
	# else:
		target = self.tree_search(p, name)
		if target:
			# print('Found target: '+target.pid)
			self.kill_tree(target)
			q = self.find_highest_priority()
			self.scheduler(q)
		else:
			# print('THe process does not exist below the running process or is not the running process')
			return 'The process does not exist below the running process or is not the running process'
		
	def find_rcb(self,rid):
		if rid=='R1':
			rcb = self.RS.r1
		elif rid=='R2':
			rcb = self.RS.r2
		elif rid=='R3':
			rcb = self.RS.r3
		else:
			rcb = self.RS.r4
		return rcb

	def request(self, rid, units):
		r = self.find_rcb(rid)
		p = self.find_highest_priority()  # fetch currently running process
		if p.pid=='init':
			# print('No request allowed on init process')
			self.scheduler(p)
			return 'No request allowed on init process'
		elif r.status.u >= int(units):  # if units are availble for the requiesting resource
			# print('Availble!!')
			r.status.u = r.status.u - int(units)  # subtract requested units from available units
			resource = Resource(r, int(units))  # make resource pack, RCB and consumed units
			p.otherResources.append(resource)  # append the resource to other resources in the runnnig PCB
			self.scheduler(p)
		else:
			# print('Not available, should wait!')
			p.status.type = 'blocked'
			p.status.list = r.waitingList
			if p.priority=='2':
				self.RL.system.remove(p)
				# r.waitingList.system.insert(p)
				r.waitingList.append((p, int(units)))  # tuple of the process and units
				q = self.RL.system.list[0]
				self.scheduler(q)
			elif p.priority=='1':
				self.RL.user.remove(p)
				# r.waitingList.user.insert(p)
				r.waitingList.append((p, int(units)))  # tuple of the process and units
				q = self.RL.user.list[0]
				self.scheduler(q)
			else:
				# print('Req, this is the p: '+str(p.priority))
				# print('Req No process running')
				return 'Req No process running'

	def release(self, rid, units, command=True):
		current = self.find_highest_priority()
		# proceed = True
		proceed = False
		if command:
			resource_at = None
			for i,resource in enumerate(current.otherResources):
				if resource.r.rid == rid:
					proceed = True
					resource_at = i
					break
		else:
			proceed = True
		if proceed:
			r = self.find_rcb(rid)
			if r.status.k < r.status.u + int(units):
				return 'Too many resources releasing'
			# listed = list(current.otherResources)
			# listed.pop(resource_at)
			# current.otherResources = deque(listed)
			r.status.u = r.status.u + int(units)			
			while r.waitingList:
				# find the consuming resource package
				req = r.waitingList[0][1]  # the units requested by the head of waiting list
				if not r.status.u >= req:
					break
				else:
					q = r.waitingList[0][0]  # the pcb of the head of waiting list
					r.status.u = r.status.u - req
					r.waitingList.pop(0)
					q.status.type = 'ready'
					q.status.list = self.RL
					resource = Resource(r, int(req)) 
					q.otherResources.append(resource)
					if q.priority=='2':
						self.RL.system.insert(q)
					elif q.priority=='1':
						self.RL.user.insert(q)
					else:
						# print('No RL level for this found.')
						pass
			p = self.find_highest_priority()
			self.scheduler(p)
		else:
			return 'Not running'

	def timeout(self):
		"""
		Invoke context switch.
		"""
		p = self.find_highest_priority()  # finding running process
		if p.priority=='2':
			self.RL.system.rotate()
			q = self.RL.system.list[0]
			self.scheduler(q)
		elif p.priority=='1':
			self.RL.user.rotate()
			q = self.RL.user.list[0]
			self.scheduler(q)
		else:
			# print('To, this is the p: '+str(p.priority))
			self.scheduler(p)
		
	def check(self):
		print('---------Manager----------')
		self.RL.check()
		self.crTree.check()
		print('--------Manager END-------')


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
	# rotate leading/ending whitespaces
	input.strip()
	# count number of args
	args = input.split()
	if not args:
		return 'no input'
	# command
	if args[0]=='init':
		if (len(args) >= 2):
			return 'init: no argument allowed'
		error = manager.init()
		return error
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
		error = manager.create(args[1], args[2])  # pid, priority
		return error
	elif args[0]=='de':
		if len(args) <= 1:
			return 'destroy: need one argument, name'
		if len(args) >= 3:
			return 'destroy: too many arguments'
		if args[1]=='init':
			return 'destroy: no destroying init process allowed'
		if is_int(args[1]):
			return 'destroy: integer, process name should be one char'
		if len(args[1]) >= 2:
			return 'destroy: too many chars, name should be one char'
		error = manager.destroy(args[1])  # pid
		return error
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
		if int(args[2]) <= 0 or int(args[2]) >= 5:
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
		error = manager.request(args[1], args[2])  # rid, units
		return error
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
		error = manager.release(args[1], args[2])
		return error
	elif args[0]=='to':
		if len(args) >= 2:
			return 'time-out: no argument allowed'
		manager.timeout()
	else:
		return 'available commands: init, cr <name> <priority>, de <name>, req <resource name> <unit>, rel <resource name> <unit>, to'
	# argument
	# parsed_input = input
	# return parsed_input

def initiate():
	manager = Manager()
	# manager.check()
	while(1):
		var = raw_input()
		shell_error_msg = parse(manager, var)
		if not shell_error_msg:
			res = manager.find_highest_priority().pid
			print(res)
			# return res
		else:
			print('error')
			# return 'error'

def call(inputs, out):
	# parse
	manager = Manager()
	out.write('init')
	out.write(' ')
	for input in inputs:
		print(input)
		if input=='':
			out.write('\n')
		# res = mo.call(line)
		# out.write(res)
		# out.write(' ')
		else:
			shell_error_msg = parse(manager, input)
			if not shell_error_msg:
				res = manager.find_highest_priority().pid
				out.write(res)
				out.write(' ')
				# return res
			else:
				out.write('error')
				out.write(' ')
				# return 'error'

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

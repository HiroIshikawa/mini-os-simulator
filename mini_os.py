import sys


def initiate():
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
	if (args[0]=='init'):
		if (len(args) >= 2):
			return 'init: no argument allowed'
		initiate()

	if (args[0]=='cr'):
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

	# argument
	parsed_input = input
	return parsed_input

def manager(input):
	# parse
	res = parse(input)
	return res


def display(res):
	print(res)

def driver(input):	
	# wait user's input
	# print(type(var))
	# call process / resource manager and receive response
	response = manager(input)
	# display output
	display(response)
	# display()

def shell():
	while(1):
		var = raw_input()
		driver(var)
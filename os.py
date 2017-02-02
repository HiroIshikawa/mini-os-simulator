import sys

def manager():
	return 'Response'

def driver():	
	# wait user's input
	var = raw_input()
	# call process / resource manager and receive response
	response = manager()
	# display output
	print(response)

def shell():
	while(1):
		driver()

# initiate manager

# activate shell
shell()
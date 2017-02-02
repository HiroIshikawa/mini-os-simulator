import mini_os as mo

import fnmatch
import sys

input = sys.argv[1]

if input.endswith('.txt'):
	with open(input) as f:
		content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip() for x in content] 

	for line in content:
		mo.driver(line)
elif input=='s':
	print("Initiate Shell Mode....")
	mo.shell()

else: 
	mo.driver(input)
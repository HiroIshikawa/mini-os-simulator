import mini_os as mo

import fnmatch
import sys

input = sys.argv[1]

# mo.initiate()

if input.endswith('.txt'):
	out = open('output.txt', 'w')
	with open(input) as f:
		content = f.readlines()
		# you may also want to remove whitespace characters like `\n` at the end of each line
		content = [x.strip() for x in content]
	mo.call(content, out)


elif input=='s':
	print("Initiate Shell Mode....")
	mo.initiate()
else: 
	mo.driver(input)
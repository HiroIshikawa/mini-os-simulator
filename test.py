import mini_os as mo

fname = 'test_input.txt'

with open(fname) as f:
	content = f.readlines()
	# you may also want to remove whitespace characters like `\n` at the end of each line
	content = [x.strip() for x in content] 

for line in content:
	mo.driver(line)
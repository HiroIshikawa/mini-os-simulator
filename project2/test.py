from sys import argv

import scheduler

input_file = argv[1]

# Read text file
with open(input_file) as f:
	content = f.readlines()

content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]

for c in content:
	scheduler.purse(c)

# for i in content:
# 	for j in i.replace(" ", ""):
# 		print(j)
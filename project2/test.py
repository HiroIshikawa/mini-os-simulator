import os
from sys import argv

input_file = argv[1]

# Read text file
with open(input_file) as f:
	content = f.readlines()

content = [x.strip() for x in content]

for i in content:
	for j in i.replace(" ", ""):
		print(j)
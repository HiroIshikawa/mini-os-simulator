from sys import argv

import vm

input_file1 = argv[1]
input_file2 = argv[2]
output_file1 = argv[3]
output_file2 = argv[4]

with open(input_file1) as f:
	lines = f.readlines()

# split inputs to st input and pt input with mapping all values to ints
st_init = map(int, lines[0].split(' '))
pt_init = map(int, lines[1].split(' '))

# print st_init
# print pt_init

# split st input into the format of pairs 
st_init_pairs = []
for i in range(len(st_init)):
	if i%2 != 0:
		st_init_pairs.append((st_init[i-1], st_init[i]))

# print st_init_pairs

# split pt input into to format of triples
pt_init_triples = []
for i in range(1,len(pt_init)+1):
	if i > 1 and i%3 == 0:
		pt_init_triples.append((pt_init[i-3], pt_init[i-2], pt_init[i-1]))

# print pt_init_triples

pm = vm.initialize_pm(st_init_pairs, pt_init_triples)


with open(input_file2) as f:
	lines = f.readlines()

# split inputs to st input and pt input with mapping all values to ints
va_translate = map(int, lines[0].split(' '))

# print st_init
# print pt_init

# split st input into the format of pairs 
va_translate_pairs = []
for i in range(len(va_translate)):
	if i%2 != 0:
		va_translate_pairs.append((va_translate[i-1], va_translate[i]))

# print va_translate_pairs

outputs = vm.translate_vm(pm, va_translate_pairs)

print outputs

# output the result without TLB
with open(output_file1, 'w') as f:
	# out_f = open(output_file1, 'w')
	for output in outputs:
		f.write(output)
		f.write(' ')
	f.close()


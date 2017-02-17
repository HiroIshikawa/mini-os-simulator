from sys import argv

import scheduler

input_file = argv[1]
output_file = argv[2]

# Read text file
with open(input_file) as f:
	content = f.readlines()

content = [x.strip() for x in content]
content = [x.replace(" ", "") for x in content]

runs = []

for c in content:
	ps = scheduler.purse(c)
	runs.append(ps)

scheduling_results = []

for run in runs:
	scheduling_results.append(scheduler.schedule(run))

print(scheduling_results)

out_f = open(output_file, 'w')

for turnarounds in scheduling_results:
	scheduler.report(out_f, turnarounds)
	out_f.write('\n')

out_f.close()
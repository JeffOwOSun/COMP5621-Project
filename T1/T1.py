import csv
import os.path
import pprint

# the default path of trace file
trace_file_dir = '../tracefiles/known'
trace_files = ['gi-1.trace','gi-2.trace']

output_list = []

for trace_file in trace_files:
	# the array to do the statistics
	src_ip_last_octet = [0] * 256
	
	with open(os.path.join(trace_file_dir, trace_file),'rU') as f: # U for universal newline
		next(f)
		my_reader = csv.reader(f, delimiter = '\t')
		for start, src_ip, src_port, dest_ip, dest_port, octets in my_reader:
			last_octet = int(src_ip.strip().split('.')[3])
			src_ip_last_octet[last_octet] += 1
	
	output_list.append(src_ip_last_octet)
	summ=float(sum(src_ip_last_octet))
	output_list.append([x/summ for x in src_ip_last_octet])

output_list = [tuple([str(x[i]) for x in output_list]) for i in range(256)]
#pprint.pprint(src_ip_last_octet)
with open('output', 'w') as f:
	f.write('last_octet\tgi-1_src\tgi-1_src_percent\tgi-2_src\tgi-2_src_percent\n')
	for i in range(256):
		f.write("%d\t%s\n" % (i, '\t'.join(output_list[i])))
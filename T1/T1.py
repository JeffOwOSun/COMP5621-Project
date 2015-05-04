import csv
import os.path
import pprint

# the default path of trace file
trace_file_dir = '../tracefiles/known'

# the array to do the statistics
src_ip_last_octet = [0] * 256
dest_ip_last_octet = [0] * 256

with open(os.path.join(trace_file_dir,'gi-1.trace'),'rU') as f: # U for universal newline
	next(f)
	my_reader = csv.reader(f, delimiter = '\t')
	for start, src_ip, src_port, dest_ip, dest_port, octets in my_reader:
		last_octet = int(src_ip.strip().split('.')[3])
		src_ip_last_octet[last_octet] += 1
		last_octet = int(dest_ip.strip().split('.')[3])
		dest_ip_last_octet[last_octet] += 1

#pprint.pprint(src_ip_last_octet)
with open('output', 'w') as f:
	#f.write("%s\n%s\n" % ('\t'.join(str(x) for x in src_ip_last_octet), '\t'.join(str(x) for x in dest_ip_last_octet)))
	for i in range(0, 255):
		f.write("%s\n" % '\t'.join((str(i), str(src_ip_last_octet[i]), str(dest_ip_last_octet[i])))) #extra bracket inside join to make a tuple
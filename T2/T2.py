import csv
import os
import pprint

def main():
	# the default path of trace file
	known_trace_file_dir = '../tracefiles/known'
	unknown_trace_file_dir = '../tracefiles/unknown'
	
	# get the files
	known_trace_files = [os.path.join(known_trace_file_dir, x) for x in os.listdir(known_trace_file_dir) if x.endswith(".trace")]
	unknown_trace_files = [os.path.join(unknown_trace_file_dir, x) for x in os.listdir(unknown_trace_file_dir) if x.endswith(".trace")]
	trace_files = known_trace_files + unknown_trace_files
	
	# process each known file
	# list of standard deviations
	gi_stdevs = []
	dc_stdevs = []
	# the list for the log
	logs = {}
	
	for index, trace_file in enumerate(trace_files): #index is only for logging the progress
		print("process file %d/%d: %s ...\n" % (index + 1, len(trace_files), trace_file.split('/')[-1]))
		#the dictionary to store the result
		log_result = {}
		#open the file
		with open(trace_file,'rU') as f: # U for universal newline
			#calculate the distribution
			src_ip_last_octet, dest_ip_last_octet = calc_last_octet_distrib(f)
			
			#calculate the standard deviation
			my_stdev = diff_stdev(src_ip_last_octet, dest_ip_last_octet)
			
			#determine the file type
			file_type = ''
			if (trace_file[0] == 'g'): #general internet traffic
				gi_stdevs.append(my_stdev)
				file_type = 'general internet'
			elif (trace_file[0] == 'd'):
				dc_stdevs.append(my_stdev)
				file_type = 'datacenter'
			else:
				file_type = 'unknown'
			
			log_result['src_ip_last_octet'] = src_ip_last_octet
			log_result['dest_ip_last_octet'] = dest_ip_last_octet
			log_result['stdev'] = my_stdev
			log_result['file_type'] = file_type
				
		logs[trace_file] = log_result
		
	###for debug use only###
	###pprint.pprint(logs)
	
	#the averaged standard deviations
	gi_stdev = avg(gi_stdevs)
	dc_stdev = avg(dc_stdevs)
	
	#save the logs
	import json
	log_string = json.dumps(logs)
	with open('output.json','w') as f:
		f.write(log_string)

##########################################
# function: calculate the distribution of the last octet of inbound and outbound traffic
# return value: (src_ip_last_octet, dest_ip_last_octet)
# parameter: file_handle: the file handle to process
##########################################
def calc_last_octet_distrib(file_handle):
	#initialize the output arrays
	src_ip_last_octet = [0] * 256
	dest_ip_last_octet = [0] * 256
	f = file_handle
	
	next(f)
	my_reader = csv.reader(f, delimiter = '\t')
	for start, src_ip, src_port, dest_ip, dest_port, octets in my_reader:
		last_octet = int(src_ip.strip().split('.')[3])
		src_ip_last_octet[last_octet] += 1
		last_octet = int(dest_ip.strip().split('.')[3])
		dest_ip_last_octet[last_octet] += 1
		
	return (src_ip_last_octet, dest_ip_last_octet)

##########################################
# function: calculate the standard deviation of the normalized difference between arr_1 and arr_2
# return value: stdev
# parameter: arr_1, arr_2 the two arrays to process
##########################################
def diff_stdev(arr_1, arr_2):
	#calculate the signed difference
	dif = [a-b for a,b in zip(arr_1, arr_2)]
	#calculate the average
	avg = [(a+b)/2 for a,b in zip(arr_1, arr_2)]
	#calculate the signed percentage difference
	dif = [a/b for a,b in zip(dif,avg)]
	#calculate the standard deviation of signed percentage difference
	return stdev(dif)

##########################################
# function: calculate the standard deviation of the given list of numbers
# return value: stdev
# parameter: numbers the list of numbers
##########################################
def stdev(numbers):
	#calculate the average
	my_avg = avg(numbers)
	#calculate the difference and square
	ret = [(x - my_avg)**2 for x in numbers]
	#calculate the mean
	ret = avg(ret)
	#take sqrt
	return ret**(0.5)
	
	
##########################################
# function: calculate the average of the given list of numbers
# return value: average
# parameter: numbers the list of numbers
##########################################
def avg(numbers):
	return sum(numbers) / float(len(numbers))

if __name__ == "__main__":
    main()
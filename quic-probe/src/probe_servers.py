from __future__ import division
import sys

from subprocess import call, check_output
from multiprocessing.dummy import Pool
from multiprocessing import Process
import argparse

#TODO: Spwan multiple processes with popen, check runtime against single run

def processIP(line):
	try:
		loggedResponse = False
		result = ''

		tries = 0
		recv_response = False
		while(not recv_response and tries < 3):
			# Try to aquire a non-TO response from the server	
			response = check_output('''echo '{"addr": "%s", "sni": "%s"}' | ./quic-grabber''' % (line.strip() + ':443', 'www.example.org'), shell=True)
			if 'HandshakeTimeout' in response:
				tries += 1
			else:
				recv_response = True

		servers = check_output('''echo '%s'  | python extract_versions.py''' % response.strip() , shell=True)

		if servers.strip() == '[]':
			result += "False,\n"
		else:
			result += "True,\n"

		#Record supported versons
		result += "%s \n" % servers.strip()

		log_trace = False

		if log_trace:
			result += " %s\n\nTraceroute:\n" % response

			tr = check_output('python tr.py %s' % line.strip(), shell=True)
			result += "%s\n" % tr

		result += "%s\n\n\n================\n\n\n" % response

		call('echo "%s" >> %s' % (result, outfname), shell=True)
	except Exception as e:
		with open('errors/%s.err' % line) as f:
			f.write(repr(e))
		

from datetime import datetime
from threading import Thread


def ipGenerator():
	with open('servers_feb') as f:
		for line in f:
			yield line


def execProbe(servers):
	print "Starting at: ", str(datetime.now())
	'''servers = []
	with open('servers_feb') as f:
		for line in f[0:chunk_size]:
			servers += [line]
			if len(servers) == chunk_size:
				break
	'''
	pool = Pool()

	for i, _ in enumerate(pool.imap(processIP, servers), 1):
	    print '\r' + str(datetime.now()) + ' ' + str((i/chunk_size)*100) + '% done',

	pool.close()
	pool.join()
	#for line in servers:
	#	processIP(line)
	print
	print 'Done'


chunk_size = 250 # 100 000
outfname = 'res/out.tst'
num_proc = 4

def main():
	if '--help' in sys.argv:
		print 'help message'
		exit(0)
	global outfname, chunk_size, num_proc

	if len(sys.argv) > 2:
		outfname = sys.argv[2]
	if len(sys.argv) > 3:
		chunk_size = int(sys.argv[3])
	if len(sys.argv) > 4:
		num_proc = int(sys.argv[4])

	sys.stdout.write("Running file with: outf={} chunk_size={} num. procs={}\n".format(outfname, chunk_size, num_proc))

	procs = []
	if len(sys.argv) > 1:
		print sys.argv[1]
		serverGenerator = ipGenerator()
		for _ in range(num_proc):
			servers = []
			while(len(servers) != chunk_size):
				servers += [serverGenerator.next()]
			p = Process(target=execProbe, args=(servers,))
			p.start()		
			procs.append(p)

		for p in procs:
			p.join()
		
		print "exec'd %d processes" % num_proc
		exit()
	
	execProbe()

if __name__ == '__main__':
	main()  

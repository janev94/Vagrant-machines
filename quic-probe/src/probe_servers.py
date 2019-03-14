from __future__ import division
import sys

from subprocess import call, check_output
from multiprocessing.dummy import Pool
from multiprocessing import Process
import argparse

#TODO: Spwan multiple processes with popen, check runtime against single run

def processIP(line):
	loggedResponse = False

	#print line.strip() + ':443'
# Need to use shell=True, as we're passing string to call()
	response = check_output('''echo '{"addr": "%s", "sni": "%s"}' | ./quic-grabber''' % (line.strip() + ':443', 'www.example.org'), shell=True) 
	servers = check_output('''echo '%s'  | python extract_versions.py''' % response.strip() , shell=True)
	if servers.strip() == '[]':
		call('echo "False", >> %s' % outfname, shell=True)
	else:
		call('echo "True", >> %s' % outfname, shell=True)

	#Record supported versons
	call('echo "%s, " >> %s' % (servers.strip(), outfname), shell=True)

	log_trace = False

	if log_trace:
		call('echo " %s\n\nTraceroute:\n" >> %s' % (response, outfname), shell=True)
		tr = check_output('python tr.py %s' % line.strip(), shell=True)
		call('echo "%s" >> %s' % (tr, outfname), shell=True)

	call('echo "%s" >> %s' % (response, outfname), shell=True)

	call('printf "\n\n\n================\n\n\n" >> %s' % outfname, shell=True)


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
		chunk_size = sys.argv[3]
	if len(sys.argv) > 4:
		num_proc = sys.argv[4]

	sys.stdout.write("Running file with: outf={} chunk_size={} num. procs={}".format(outfname, chunk_size, num_proc))

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

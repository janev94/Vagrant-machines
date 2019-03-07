from subprocess import call, check_output
from multiprocessing.dummy import Pool

def processIP(line):
	loggedResponse = False

	print line.strip() + ':443'
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



outfname = 'res/out'

servers = []
with open('servers_feb') as f:
	for line in f:
		servers += [line]
		if len(servers) == 250:
			break

pool = Pool()

pool.imap(processIP, servers)

pool.close()
pool.join()
#for line in servers:
#	processIP(line)

print 'Done'  

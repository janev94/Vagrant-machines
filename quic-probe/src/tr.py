#!/usr/bin/python

import socket
import struct
import sys

# We want unbuffered stdout so we can provide live feedback for
# each TTL. You could also use the "-u" flag to Python.
class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = flushfile(sys.stdout)

def main(dest_name):
    dest_addr = dest_name
    port = 443
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    curr_addr = None
    while not (curr_addr == dest_addr or ttl > max_hops):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TOS, 1)
        
        
        # Set the receive timeout so we behave more like regular traceroute
        recv_socket.settimeout(0.1)        

        recv_socket.bind(("", port))
        sys.stdout.write(" %d  " % ttl)
        send_socket.sendto("", (dest_name, port))
        curr_addr = None
        curr_name = None
        finished = False
        tries = 3
        while not finished and tries > 0:
            try:
                # Check recv'd data and keep receiving ICMPs until timeout or an answer for the sent one is received
                recv_data, curr_addr = recv_socket.recvfrom(512)
                icmp_hdr = recv_data[20:28]
                icmp_pl = recv_data[28] + recv_data[29]
                t, code, checksum, _ = struct.unpack('bbHI', icmp_hdr)
                ver, ecn = struct.unpack('BB', icmp_pl)
#		sys.stdout.write("type: %s code: %s checksum: %s \n" % (t, code, checksum))
                ecn = ecn & 0b00000011 # get the last two bits of ToS field to extract ECN
                sys.stdout.write("ecn: %d " % ecn)
                finished = True
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except IOError as e:
                if(isinstance(e, socket.timeout)):
                    tries = tries - 1
                    sys.stdout.write("* ")
        
        send_socket.close()
        recv_socket.close()
        
        if curr_addr is not None:
            curr_host = "%s (%s)" % (curr_name, curr_addr)
        else:
            curr_host = ""
        sys.stdout.write("%s\n" % (curr_host))

        ttl += 1

if __name__ == "__main__":
	main(sys.argv[1])
	#main('google.com')

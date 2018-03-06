import socket
import sys
from pyMultiwii import MultiWii

# Some Gloabals
host = 'localhost'

if __name__ == '__main__':
	# Initiate the MWC
	board = MultiWii("/dev/ttyUSB0")

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	# Bind and listen for connections 
	server_address = (host, 10001)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)
	sock.listen(1)

	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	print >>sys.stderr, 'client connected:', client_address
	data = 'init'
	try:
	    while data!="":
		data = connection.recv(19)
		print >>sys.stderr, 'received "%s"' % data
		pwmValues = data.split()
		board.sendCMD(8,MultiWii.SET_RAW_RC,pwmValues)
		#print board.getData(MultiWii.MOTOR)
	finally:
	    connection.close()

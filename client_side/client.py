from socket import *
from time import *
kp = 'keep alive'

def client_socket():
	"""
	Water Station Project
	Set up client-side socket connection
	"""
	HOST = '127.0.0.1'
	PORT = 20000
	with socket(AF_INET, SOCK_STREAM) as s:
		try:
			s.connect((HOST, PORT))
			print("Connected to host {} at port {}".format(HOST, PORT))
		except:
			print("entered port 20005")
			s.connect((HOST, PORT + 5))
			print("Connected to host {} at port {}".format(HOST, PORT + 5))
		while True:
			incoming = s.recv(1024)
			
			if incoming:
				print("Received message")
			else:
				print("The server has dis-connected")
				s.close()
				break
				
			if incoming.decode() == kp:
				print("Keep alive request received")
				station_setup("status.txt")
				current_status = read_from_station()
				s.send(current_status.encode())
				print("Station status sent to server\n")
			elif incoming.decode() == "fix data":
				print("Server closed connection.\n")
				print("Data format incorrect. Please make correction and connect again.")
				break
			else:	
				s.send("Leave me alone, i'm resting".encode())

#~ Station setup function defs START
def station_setup(station_file):
	"""
	station_setup
	"""
	global station_object
	station_object = open(station_file, 'r')
		
def read_from_station():
	status = station_object.readline()
	return status
	
def close_station():
	station_object.close()
#~ Station setup function defs END

#~ Start Main
if __name__ == '__main__':
	client_socket()

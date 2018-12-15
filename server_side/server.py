from socket import *
from time import *
from sqlite3 import *
import datetime
import _thread as thread

client_list = []
mythread = 0
kp = 'keep alive'

#~ Socket functions defs START
def client_conn(sock):
	"""
	Accept client
	"""
	(conn, address) = sock.accept()
	global mythread
	mythread += 1
	print("\nConnected to Client #{}: {}".format(mythread, address[1]))
	return (conn, address)

def sqlite3_send_keep_alive(conn, addr, mythread):
	"""
	Send 'keep alive' request
	"""
	conn_rep = conn.__repr__().split()
	while conn_rep[1] != "[closed]":
		try:
			disconnect_type = 0
			conn.send(kp.encode())
			data = conn.recv(1024)
			data = data.decode().split()
			''' Handle data -> checks data format for
				1) If received 3 values, not more & not less
				2) If all values are integers
				3) If 1st value is 3 digits long, not more & not less
				4) If 2nd value is 1 digit long, not more & not less
				5) If 3nd value is 1 digit long, not more & not less
				If data format incorrect, raises ValueError, sends message to client, & dis-connects the client
			'''
			if ((len(data) == 3) and data[0].isdigit() and
			len(data[0]) == 3 and data[1].isdigit() and
			len(data[1]) == 1 and data[2].isdigit() and
			len(data[2]) == 1):
				pass
			elif data == []:
				raise ValueError("Received empty message, client has dis-connected")
			else:
				disconnect_type = 1
				raise ValueError("Received data in incorrect format")

			print("Receiving data from Client #{}: {}".format(mythread, conn_rep[8][:-2]))
			print("Data received:\t{}".format(data))
			if data:
				t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
				data_tuple = data[0], t, data[1], data[2]
				curs, conn_sql = sqlite3_db_setup("data.sqlite3")
				sqlite3_create_table(curs)
				sqlite3_insert_data(curs, conn_sql, data_tuple)
				print("Finished writing to db_sqlite3 {} \n".format(data_tuple))
				conn_rep = conn.__repr__().split()
				sleep(5)
		except:
			if disconnect_type == 1:
				print("Client #{} data in poor format".format(mythread))
				conn.send("fix data".encode())
				print("Server has now dis-connected from Client #{}, {}\n".format(mythread, addr))
			else:
				print("Client #{}, {} has dis-connected\n".format(mythread, addr))
			break
#~ Socket function defs END

#~ Data Base setup functions START

def sqlite3_db_setup(data_file):
	conn = connect(data_file)
	curs = conn.cursor()
	return curs, conn

def sqlite3_create_table(curs):
	curs.execute('''CREATE TABLE IF NOT EXISTS station_status
	(station_id INT PRIMARY KEY,
	last_date TEXT,
	alarm1 INT,
	alarm2 INT)
	''')

def sqlite3_insert_data(curs, conn, data):
	entry = "INSERT OR REPLACE INTO station_status VALUES (?, ?, ?, ?)"
	curs.execute(entry, data)
	conn.commit()
	conn.close()
#~ Data Base setup functions END

#~ Start Main
if __name__ == '__main__':
	with socket(AF_INET, SOCK_STREAM) as sock:
		# Make second port option available in case the first is being used
		try:
			sock.bind(("", 20000))
			sock.listen(0)
		except OSError:
			sock.bind(("", 20005))
			sock.listen(0)
		print("Socket connection now open\n")
		while True:
			(conn, address) = client_conn(sock)
			client_list.append(mythread)
			print("Full client list:", client_list)
			thread.start_new_thread(sqlite3_send_keep_alive, (conn, address, mythread))

#~ End Main

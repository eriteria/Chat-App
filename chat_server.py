import socket
#for monitoring
import select

#for later use
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Minor change: to allow us to reuse adresses
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Starting the server
server_socket.bind((IP, PORT))
server_socket.listen()
#to keep track of our clients
sockets_list = [server_socket]
#list of 
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False
#but bytes are unlimited
#who are you learning from sentdex?
#OMG yes 
#sentdex is the only guy i really understand he and tech with tim they are my idols
#i also learnt sockets under sentdex
#Basically is the server complete ??
#we want it to act as a pipe through multiple clients??
#No, it is not done, but this server will act like a mass broadcaster, but we

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        #when the server receives a message it notifies all the clients including the sender
        #this also accepts new connections
        if notified_socket == server_socket:
            #if it is a new connection we accept it here
            client_socket, client_address = server_socket.accept()
            #this part sets the username of the new client which the client will send as the first message(by fault, we will set thatde)
            user = receive_message(client_socket)
            #just incase we dont receive anything we want to continueet)
            if user is False:
                continue       
            #then finally add the client to our list of clients 

            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            #let me explain all this
#am getting it .....keep going so basically because i dont understand your concept of sockets you will work on the client side too,,,,,and i will work on the GUI mostly
# yeah i agree to that
        #time to receive some messageselse:    
        else:
            message = receive_message(notified_socket)
            if message is False:
                #client disconnected
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                #remove from active socket
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            #get the username of the client
            user = clients[notified_socket]
            
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            #distribute messages across all other
            for client_socket in clients:
#open the other file so that i can continue with the GUI
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:

        sockets_list.remove(notified_socket)
        del clients[notified_socket]
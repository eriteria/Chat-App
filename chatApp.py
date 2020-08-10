#we will need sockets ,,, and tkinter for GUI
#lemme import those 
import socket
from tkinter import *
from tkinter import ttk
import select
import errno

#socket constants
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

#socket initialisation
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)


#ok....ill initialize gui first
#New chat window

def chat_window():
    print("I work")
    connect(e1.get())

#send message function
def send(message): 
    if message:
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        #organising the message and preparing it for sending
        #Note: Username not needed because the server saves the username as long as you're connected
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        #Sending message
        client_socket.send(message_header + message)

#function to connect to server. This should be the first function to be executed before sending/receiving
def connect(my_username):
    #Setting username
    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    #sending username to server
    client_socket.send(username_header + username)

#function to receive messages
def receive():
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            #if we stop receiving data, the server is most likely down
            if not len(username_header):
                ret = "connection closed by server"
                print(ret)
                sys.exit() #this is prone to change
                return ret
                            
            #receiving username of sender
            username_length = int(username_header.decode('utf-8').strip())
            
            username = client_socket.recv(username_length).decode('utf-8')
            #Receiving message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            ret = f'{username} > {message}'
            return ret
    #for sake of practice and hassle-free operation
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            ret = f'Reading error: {str(e)}'
            return ret
            sys.exit()


root = Tk()
root.title("Chat_App")
root.geometry('400x400')

l1 = Label(root, text="Enter Username: ", font=('Courier',12,'bold'))
l1.place(x=10, y=50)
e1 = Entry(root, width="25", bg="white")
e1.place(x=170, y=50)
b1 = ttk.Button(root, text="Connect", command=chat_window)
b1.place(x=210, y=90)

#


#cant i run it 
#you can, i think, try
#nop its says no such file directory but that is because there is no dir like that in my pc




#lemme restart my router it is down and then i need to install python modules again
#oh okay but im running it now do you see anything happening?








root.mainloop()
#initialize sockets
#this part is to initialize the socket and set it to ipv4
#so you will create the server?? i was thinking we create a server first then the client later ????
# what do you think
#Yeah, we can start from there, but we have to switch back and forth because they work hand in hand
#Let me create the file for the server
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#here is to sonnect the socket to the server you want and the port
#s.connect(127.0.0.1, 80)
#lets do this 
#You in ??
#I can't seem to find the file for the server

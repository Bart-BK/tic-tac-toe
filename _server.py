import socket
import select
from sys import argv

SOCKET_LIST = [];
RECV_BUFFER = 4096;

def chat_server():
    if(len(argv) < 2):
        print ("Use : python _server.py hostname port");
        exit(); 
    elif(len(argv) == 2):
        HOST = "";
        PORT = argv[1];
    elif(len(argv) == 3):
        HOST = argv[1];
        PORT = argv[2];

    CONNECTION = (HOST, int(PORT));

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

    while True:
        try:
            server_socket.bind(CONNECTION);
            server_socket.listen(1);
            break;
        except:
            print ("There is an error in bind "+HOST+"::"+PORT);
            chose = input("[A]bort, [C]hange ou [T]ry again?");

            if(chose.lower() == 'a'):
                exit();
            elif(chose.lower() == 'c'):
                    HOST = input("Enter the HOST: ");
                    PORT = input("Enter the PORT: ");

    
    match = [2];
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print ("Bind done, waiting connections in "+HOST+"::"+PORT);
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                if(len(match) != 3):
                    SOCKET_LIST.append(sockfd)
                print ("Player (%s, %s) connected" % addr);
                match.append(sock);
                broadcast(server_socket, sockfd, "[Adversario] entrou no seu jogo\n");
                if(len(match) == 3):
                    broadcast(server_socket, server_socket, "\n\nO jogo iniciou\n\n");
                    SOCKET_LIST[1].send("[SERVER] You are the \'X\'\n\n");
                    SOCKET_LIST[2].send("[SERVER] You are the \'O\'\n\n");


            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER);
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[Adversario] ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock);

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    exit(chat_server()) 
# Import from sys 
from sys import argv, stdin, stdout
# Import sockets
import socket
# Import select
import select
# Import OS
import os

# Client socket
def tic_tac_toe_client():
	# Using parameter to define HOST and PORT
	# Case less or more than expected
	if((len(argv) <= 2) or (len(argv)) > 4): 
		print ("Use : python _client.py hostname port language(BR|EN) ");
		exit();	
	# Case HOST and PORT given by command line, but not language
	elif(len(argv) == 3):
		HOST = argv[1];
		PORT = argv[2];
		LANGUAGE = "EN";
	# Case HOST, PORT and LANGUAGE given by command line
	elif(len(argv) == 4):
		HOST = argv[1];
		PORT = argv[2]; 
		if(argv[3].lower() != "br" and argv[3].lower() != "en"):
			LANGUAGE = input("Please, give a valid language:");
			while(LANGUAGE.lower() != "br" and LANGUAGE.lower() != "en"):
				LANGUAGE = input("Please, give a valid language (BR or EN):");
		else:
			LANGUAGE = argv[3];

	# Set interface
	LANGUAGE = LANGUAGE.lower();
	if(LANGUAGE == "br"):
		print("Interface esta definida para PT-BR");
	else:
		print("Interface is set to EN");

	# Define connection
	CONNECTION = (HOST, int(PORT));

	# Create a TCP/IP socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	# Set timeout connection
	client_socket.settimeout(10);

	while True:
		# If still having trouble with connection, recall the loop
		try:
			if(LANGUAGE == "br"):
				print ("\nConectando a "+HOST+"::"+PORT);
			else:
				print ("\nConnecting to "+HOST+"::"+PORT);

			# Try connect in HOST and PORT given
			client_socket.connect(CONNECTION);
			break;
		except:
			# If have any trouble, the user can change HOST or PORT
			if(LANGUAGE == "br"):
				print ("Erro ao se conectar a "+HOST+"::"+PORT);
				chose = input("[A]bortar, [M]odificar ou [T]entar novamente?");
			else:
				print ("Error in connection "+HOST+"::"+PORT);
				chose = input("[A]bort, [C]hange ou [T]ry again?");
			# Choice is abort
			if(chose.lower() == 'a'):
				exit();
			# Choice is change
			elif((chose.lower() == 'm' and LANGUAGE == "br") or (chose.lower() == 'c' and LANGUAGE == "en")):
				if(LANGUAGE == "br"):
					HOST = input("Insira o HOST: ");
					PORT = input("Insira a PORTA: ");
				else:
					HOST = input("Enter the HOST: ");
					PORT = input("Enter the PORT: ");
			else:
				continue;

	# The connection was successfull
	if(LANGUAGE == "br"):
		print ("Conexao estabelecida\nAguardando adversario...");
	else:
		print ("Connection established\nWaiting other player...");
		
	while 1:
	    socket_list = [stdin, client_socket];
	     
	    # Get the list sockets which are readable
	    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
	     
	    for sock in ready_to_read:             
	        if sock == client_socket:
	            # Incoming position from remote server
	            # Clear the console (works in linux and windows)
	            os.system('cls' if os.name=='nt' else 'clear');
	            # Receive the message
	            data = sock.recv(4096);
	            if not data :
	            	# Some trouble ...
	                print ('\nDisconnected from game\n');
	                exit();
	            else :
	                # Print message
	                stdout.write(data);
	        
	        else :
	            # User entered a position
				msg = stdin.readline();
				# Send the position to server
				client_socket.send(msg);
				# Clear buffer
				stdout.flush();

if __name__ == "__main__":

    exit(tic_tac_toe_client());
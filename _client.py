from sys import argv, stdin, stdout
import socket
import select
import os
 
def tic_tac_toe_client():
	if((len(argv) <= 2) or (len(argv)) > 4):
		print ("Use : python _client.py hostname port language(BR|EN) ");
		exit();	
	elif(len(argv) == 3):
		HOST = argv[1];
		PORT = argv[2];
		LANGUAGE = "EN";
	elif(len(argv) == 4):
		HOST = argv[1];
		PORT = argv[2]; 
		if(argv[3].lower() != "br" and argv[3].lower() != "en"):
			LANGUAGE = input("Please, give a valid language:");
			while(LANGUAGE.lower() != "br" and LANGUAGE.lower() != "en"):
				LANGUAGE = input("Please, give a valid language (BR or EN):");
		else:
			LANGUAGE = argv[3];

	LANGUAGE = LANGUAGE.lower();
	if(LANGUAGE == "br"):
		print("Interface esta definida para PT-BR");
	else:
		print("Interface is set to EN");

	CONNECTION = (HOST, int(PORT));

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	client_socket.settimeout(10);

	while True:
		try:
			if(LANGUAGE == "br"):
				print ("\nConectando a "+HOST+"::"+PORT);
			else:
				print ("\nConnecting to "+HOST+"::"+PORT);

			client_socket.connect(CONNECTION);
			break;
		except:
			if(LANGUAGE == "br"):
				print ("Erro ao se conectar a "+HOST+"::"+PORT);
				chose = input("[A]bortar, [M]odificar ou [T]entar novamente?");
			else:
				print ("Error in connection "+HOST+"::"+PORT);
				chose = input("[A]bort, [C]hange ou [T]ry again?");

			if(chose.lower() == 'a'):
				exit();
			elif((chose.lower() == 'm' and LANGUAGE == "br") or (chose.lower() == 'c' and LANGUAGE == "en")):
				if(LANGUAGE == "br"):
					HOST = input("Insira o HOST: ");
					PORT = input("Insira a PORTA: ");
				else:
					HOST = input("Enter the HOST: ");
					PORT = input("Enter the PORT: ");

	if(LANGUAGE == "br"):
		print ("Conexao estabelecida");
		#stdout.write('[Eu] '); stdout.flush();
	else:
		print ("Connection established");
		#stdout.write('[Me] '); stdout.flush();
		
	while 1:
	    socket_list = [stdin, client_socket];
	     
	    # Get the list sockets which are readable
	    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
	     
	    for sock in ready_to_read:             
	        if sock == client_socket:
	            # incoming message from remote server, s
	            os.system('cls' if os.name=='nt' else 'clear');
	            data = sock.recv(4096);
	            if not data :
	                print ('\nDisconnected from chat server');
	                exit()
	            else :
	                #print data
	                stdout.write(data);
	                """
	                if(LANGUAGE == "br"):
	                	stdout.write('[Eu] '); stdout.flush();
                	else:
                		stdout.write('[Me] '); stdout.flush(); 
            		"""
	        
	        else :
	            # user entered a message
				msg = stdin.readline();
				client_socket.send(msg);
				"""
				if(LANGUAGE == "br"):
					stdout.write('[Eu] '); 
				else:
					stdout.write('[Me] ');
				"""
				stdout.flush();

if __name__ == "__main__":

    exit(tic_tac_toe_client())
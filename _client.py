# Import from sys 
from sys import argv, stdin, stdout
# Import sockets
import socket
# Import select
import select
# Import OS
import os

# Client socket
class Client_Tic_Tac_Toe:
	"""This is a client who is connected with the socket server and is Player of the Tic Tac Toe Game"""

	def __init__(self):
		# Create a TCP/IP socket
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		# Set timeout connection
		self.client_socket.settimeout(10);

	def get_HOST_PORT(self):
		# Case HOST and PORT given by command line
		if(len(argv) == 3):
			HOST = argv[1];
			PORT = argv[2];
		# Else, request the input for the HOST and PORT
		else:
			print("Failed to get the HOST and PORT\n");
			HOST = raw_input("Enter the HOST: ");
			PORT = raw_input("Enter the PORT: ");

		# Return the HOST and PORT
		return HOST,PORT;

	def connect(self, HOST, PORT):
		# Define connection
		try:
			CONNECTION = (HOST, int(PORT));
		except:
			# If CONNECTION not receive an int
			while(self.isNotInt(PORT, "PORT")):
				PORT = raw_input("Enter the PORT (must be int): ");
			CONNECTION = (HOST, int(PORT));

		print("Connecting to "+HOST+"::"+PORT);

		try:
			# Try connect in HOST and PORT given
			self.client_socket.connect(CONNECTION);
			print("Connection established, waiting for opponent...");

		except:
			print ("Error in connection "+HOST+"::"+PORT);
			# If have any trouble, try receive again
			choice = raw_input("[A]bort, [C]hange ou [T]ry again?");
			# Choice is abort
			if(choice.lower() == "a"):
				exit();
			# Choice is change
			elif(choice.lower() == "c"):
				HOST = raw_input("Enter the HOST: ");
				PORT = raw_input("Enter the PORT: ");
			
			self.connect(HOST,PORT);

	def clear(self):
		# Clear the console (works in linux and windows)
		os.system('cls' if os.name=='nt' else 'clear');

	def recv(self, sock):
		# Receive a message from socket
		return sock.recv(4096);

	def isNotInt(self, value, typeVerification):
		if(typeVerification == "POS"):
			try:
				if(int(value) > 0 and int(value) < 10):
					return False;
				return True;
			except: # The value isn't a int type
				return True;
		elif(typeVerification == "PORT"):
			try:
				if(int(value) > 0):
					return False;
				return True;
			except: # The value isn't a int type
				return True;

	def start(self):

		while 1:
			# Socket list [key, value]
			socket_list = [stdin, self.client_socket];

			# Get the list sockets which are readable
			ready_to_read,ready_to_write,in_error = select.select(socket_list , [], []);
		     
			for sock in ready_to_read:
				# If sock is this client        
				if sock == self.client_socket:
					# Incoming position from remote server

					# Receive the message
					data = self.recv(sock);
					# Decode the received data
					data = data.decode();

					if not data :
						# Some trouble ...
						print ('\nDisconnected from game\n');
						exit();
					else :
						# Clear the console
						self.clear();
						try:
							# If received a block command, dont print the command
							if(data[0] == "B"):
								print(data[1:]);
							else:
								# Print message
								print(data);

						except Exception as e:
							print(str(e));
						

				else :
					# User entered a position
					position = raw_input();
					# Check if user entered a quit command
					if(position.lower() == "quit"):
						print("You QUIT the Game, you lost!\nGame Over");
						exit();
					# Check if the user enter a invalid position
					while self.isNotInt(position, "POS"):
						position = raw_input("Please, enter a valid position (1 to 9): ");
						# Check if user entered a quit command
						if(position.lower() == "quit"):
							print("You QUIT the Game, you lost!\nGame Over");
							exit();

					# If client is blocked, don't send the message
					if(data[0] != "B"):
						# Send the position to server
						self.client_socket.send(position.encode());
					else:
						print("It's not your turn, please wait!");
					# Clear buffer
					stdout.flush();

def main():
	title = " _____ ___ ____   _____  _    ____   _____ ___  _____ \n"\
			"|_   _|_ _/ ___| |_   _|/ \  / ___| |_   _/ _ \| ____|\n"\
			"  | |  | | |       | | / _ \| |       | || | | |  _|  \n"\
			"  | |  | | |___    | |/ ___ \ |___    | || |_| | |___ \n"\
			"  |_| |___\____|   |_/_/   \_\____|   |_| \___/|_____|\n"\
			"                                                      \n\n";

	welcome_message =	"(1) Start the Game\n"\
						"(2) Credits\n"\
						"(3) Quit\n\n";

	# Display a welcome message
	choice = raw_input(title + welcome_message);

	while True:
		try:
			# Start the game
			if(int(choice) == 1):
				# Main class of Tic Tac Toe
				client = Client_Tic_Tac_Toe();

				# Get the HOST and PORT
				HOST, PORT = client.get_HOST_PORT();

				# Try connect
				client.connect(HOST,PORT);

				# Start the Player socket
				client.start();

				exit();

			# Show Credits
			elif(int(choice) == 2):
				credits = "\nGame made by: Prabhat Kumar de Oliveira\n";
				choice = raw_input(title + credits + welcome_message);

			# Exit
			elif(int(choice) == 3):
				print("Have you liked the game?\n");
				exit();

			# Invalid choice (if int)
			else:
			    while((int(choice) < 1) or (int(choice) > 3)):
			        choice = raw_input("Please, enter valid choice: ");

        # Invalid choice (if not int)
		except Exception as e:
			choice = raw_input("Invalid choice, please enter again (must be int): ");
	

if __name__ == "__main__":

    main();
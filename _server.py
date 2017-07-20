# Import sockets
import socket
# Import select
import select
# Import argv
from sys import argv 
# Import random (to select who starts)
import random

class Server_Tic_Tac_Toe:
    """This is the server, and the game logic of tic tac toe"""

    def __init__(self):
        # Create a TCP/IP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        # Set socket options
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
        # The server will know the players roles
        self.player1_role = "";
        self.player2_role = "";
        # Content of board
        self.boardContent = list("         ");
        # Example print on screen
        self.boardTutorial = list("123456789");

    def get_PORT(self):
        # The HOST can bind all (not necessary especific host);
        HOST = "";

        # If parameters is given
        if(len(argv) == 2):
            PORT = argv[1];
        else:
            print("Failed to get the PORT\n");
            PORT = raw_input("Enter the PORT: ");

        # Return the HOST and PORT
        return HOST,PORT;

    def bind(self, HOST, PORT):
        # Define connection
        try:
            CONNECTION = (HOST, int(PORT));
        except:
            # If CONNECTION not receive an int
            while(self.isNotInt(PORT)):
                PORT = raw_input("Enter the PORT (must be int): ");
            CONNECTION = (HOST, int(PORT));

        while True:
            # Try bind
            try:
                self.server_socket.bind(CONNECTION);
                self.server_socket.listen(1);

                print("Bind done, waiting for players...");
                break;

            except Exception as e:
                # If have any trouble
                print ("There is an error in bind "+PORT+ str(e));
                choice = raw_input("[A]bort, [C]hange ou [T]ry again?");

                # If choice is abort
                if(choice.lower() == 'a'):
                    exit();
                # If choice is change
                elif(choice.lower() == 'c'):
                    PORT = raw_input("Enter the PORT: ");

                self.bind(HOST,PORT);



    def isNotInt(self, value):
        try:
            if(int(value) > 0):
                return False;
            return True;
        except: # The value isn't a int type
            return True;

    def close(self):
        # Close the socket server
        self.server_socket.close();

    def start(self):
        # Array of sockets
        socket_list = [];
        # Add server socket object to the list of readable connections
        socket_list.append(self.server_socket);
        
        while True:
            # Get the list sockets which are ready to be read through select
            ready_to_read,ready_to_write,in_error = select.select(socket_list,[],[],0);

            for sock in ready_to_read:
                # A new connection request recieved
                if sock == self.server_socket: 
                    # Accept the connection
                    sockfd, addr = self.server_socket.accept();
                    # If socket_list not have 2 players yet
                    if(len(socket_list) < 3):
                        socket_list.append(sockfd);
                        # Print on the server who connected
                        print("Player (%s, %s) connected" % addr);

            if(len(socket_list) == 3):
                self.main_loop(socket_list);
                # When main loop finish, the game will be finished too
                break;
                        

    def main_loop(self, match):
        
        RECV_BUFFER = 1024;

        # Who will start
        turn = (self.getRandomNumber())%2;
        
        player1 = match[1];
        player2 = match[2];

        self.send(player1, player2,"", "", "START");
        
        while True:
            try:
                # Try receive a position from player
                if(turn == 0):
                    self.send(player1, player2, self.player1_role, self.player2_role, "MOVE");
                    position = player1.recv(RECV_BUFFER);
                elif(turn == 1):
                    self.send(player2, player1, self.player2_role, self.player1_role,"MOVE");
                    position = player2.recv(RECV_BUFFER);

                # Received something
                if(position):
                    if(turn == 0):
                        # If the moving player cheat
                        while(self.boardReplace(self.boardContent, int(position)-1, self.player1_role) == 0):
                            self.send(player1, player2, self.player1_role, "", "CHEAT");
                            position = player1.recv(RECV_BUFFER);

                        # Check if the role results in a win
                        result, winningPath = self.checkWinner(self.boardContent, self.player1_role);
                        # If the game ends, send the winning path (or draw)
                        if result >= 0:
                            self.send(player1, player2, "", "", str(result)+winningPath);
                            exit();
                        # Else, change the turn
                        turn = 1;
                    elif(turn == 1):
                        # If the moving player cheat
                        while(self.boardReplace(self.boardContent, int(position)-1, self.player2_role) == 0):
                            self.send(player2, player1, self.player2_role, "", "CHEAT");
                            position = player2.recv(RECV_BUFFER);

                        # Check if the role results in a win
                        result, winningPath = self.checkWinner(self.boardContent, self.player2_role);
                        # If the game ends, send the winning path (or draw)
                        if result >= 0:
                            self.send(player2, player1, "", "", str(result)+winningPath);
                            exit();
                        # Else, change the turn
                        turn = 0;

            # If gone bad
            except Exception as e:
                print(str(e));
        # CONTINUE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def send(self, playerInMove, playerWaiting, moveRole, waitRole, typeMSG):
        try:
            if(typeMSG == "START"):
                # Get random number to decides the Roles
                randomNumber = self.getRandomNumber();
                # Send the Roles to respective Players
                if(randomNumber % 2 == 0):
                    self.player1_role = "O";
                    self.player2_role = "X";
                else:
                    self.player1_role = "X";
                    self.player2_role = "O";
                # The game started
                playerInMove.send("The game started, if you want quit, write \"quit\"\n");
                playerWaiting.send("The game started, if you want quit, write \"quit\"\n");
            
            # The player was cheating
            if(typeMSG == "CHEAT"):
                playerInMove.send("My role is: "+moveRole+"\nBoard Tutorial\n"+self.printBoard(self.boardTutorial)+"\nBoard Content\n"+self.printBoard(self.boardContent)+"You are trying to pick a position not empty, try again: ");
            
            if(typeMSG == "MOVE"):
                # For moving player, send the board tutorial and board content
                # For the waiting player, send the board content
                playerInMove.send("My role is: "+moveRole+"\nBoard Tutorial\n"+self.printBoard(self.boardTutorial)+"\nBoard Content\n"+self.printBoard(self.boardContent)+"Its your turn, make a move: ");
                # The message will be sent with a command, who block the client of send a position if it's not their turn
                # The command is "B" (BLOCK)
                playerWaiting.send("B"+"My role is: "+waitRole+"\nBoard Content\n"+self.printBoard(self.boardContent)+"Waiting the opponent's move");
            
            # The game result in a draw
            if(typeMSG[0] == "0"):
                playerInMove.send("Game Over\nResult in a Draw\n");
                playerWaiting.send("Game Over\nResult in a Draw\n");

            # Someone win
            elif(typeMSG[0] == "1"):
                playerInMove.send("You"+typeMSG[1:]+"\nGame Over\n");
                playerWaiting.send("You LOSE\nThe opponent"+typeMSG[1:]+"\nGame Over\n");
                exit();
        except:
            print("The moving player disconnected, the game will be finished\n");
            exit();

    def getRandomNumber(self):
        return random.randrange(2000);
    
    def checkWinner(self, board, role):
        # Check Lines
        if (len(set([board[0], board[1], board[2], role])) == 1):
            return 1, " WIN in positions 1|2|3";
        if (len(set([board[3], board[4], board[5], role])) == 1):
            return 1, " WIN in positions 4|5|6";
        if (len(set([board[6], board[7], board[8], role])) == 1):
            return 1, " WIN in positions 7|8|9";

        # Check Columns
        if (len(set([board[0], board[3], board[6], role])) == 1):
            return 1, " WIN in positions 0|3|6";
        if (len(set([board[1], board[4], board[7], role])) == 1):
            return 1, " WIN in positions 1|4|7";
        if (len(set([board[2], board[5], board[8], role])) == 1):
            return 1, " WIN in positions 2|5|8";

        # Check Diagonals
        if (len(set([board[0], board[4], board[8], role])) == 1):
            return 1, " WIN in positions 1|5|9";
        if (len(set([board[6], board[4], board[2], role])) == 1):
            return 1, " WIN in positions 3|5|7";

        # If not empty slots left, draw
        if " " not in board:
            return 0, "DRAW\n\n";

        return -1, "";


    def printBoard(self, board):
        return ("|" + board[0] + "|" + board[1]  + "|" + board[2] + "|\n" 
                + "|" + board[3] + "|" + board[4]  + "|" + board[5] + "|\n" 
                + "|" + board[6] + "|" + board[7]  + "|" + board[8] + "|\n");
        
    def boardReplace(self, board, position, role):
        # Verify if the position is empty
        if board[position] == " ":
            board[position] = role;
            return 1;
        return 0;

    # server__match_send messages to all connected clients
    def server__match_send (self, server_socket, sock, message):
        for socket in MATCH:
            # send the message only to peer
            if socket != server_socket and socket != sock :
                try :
                    socket.send(message);
                except :
                    # broken socket connection
                    socket.close();
                    # broken socket, remove it
                    if socket in MATCH:
                        MATCH.remove(socket);
 
def main():
    title = " _____ ___ ____   _____  _    ____   _____ ___  _____ \n"\
            "|_   _|_ _/ ___| |_   _|/ \  / ___| |_   _/ _ \| ____|\n"\
            "  | |  | | |       | | / _ \| |       | || | | |  _|  \n"\
            "  | |  | | |___    | |/ ___ \ |___    | || |_| | |___ \n"\
            "  |_| |___\____|   |_/_/   \_\____|   |_| \___/|_____|\n"\
            "                                                      \n\n";

    welcome_message =   "(1) Start host the Game\n"\
                        "(2) Credits\n"\
                        "(3) Quit\n\n";

    # Display a welcome message
    choice = raw_input(title + welcome_message);

    while True:
        try:
            # Start host
            if(int(choice) == 1):
                # Main class of the Tic Tac Toe Server
                server = Server_Tic_Tac_Toe();

                # Get the HOST and PORT
                HOST, PORT = server.get_PORT();

                # Try bind
                server.bind(HOST, PORT);

                # Start the Server socket
                server.start();

                # Close the Server socket
                server.close();

                exit();

            # Show credits
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
            # REMOVER !!!!!!!!!!!!!!!!!!

if __name__ == "__main__":

    main();
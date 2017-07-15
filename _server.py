# Import sockets
import socket
# Import select
import select
# Import argv
from sys import argv 
# Import random (to select who starts)
import random

MATCH = [];
RECV_BUFFER = 4096;

# The socket server
def tic_tac_toe_server():
    # If parameters is not exactly than expected
    if(len(argv) != 2):
        print ("Use : python _server.py port");
        exit(); 
    # If parameters is given
    elif(len(argv) == 2):
        HOST = "";
        PORT = argv[1];

    # Set connection
    CONNECTION = (HOST, int(PORT));

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    # Set socket options
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

    # Try bind
    while True:
        try:
            server_socket.bind(CONNECTION);
            server_socket.listen(1);
            break;
        except:
            # If have any trouble
            print ("There is an error in bind "+HOST+"::"+PORT);
            chose = raw_input("[A]bort, [C]hange ou [T]ry again?");

            # If choice is abort
            if(chose.lower() == 'a'):
                exit();
            # If choice is change
            elif(chose.lower() == 'c'):
                    HOST = raw_input("Enter the HOST: ");
                    PORT = raw_input("Enter the PORT: ");
            # If chouce is try again
            else:
                continue;

    # In this game, we will have a socket_list with 2 players;
    socket_list = [2];
    # Content of board
    boardContent = list("         ");
    # Example print on screen
    boardTutorial = list("123456789");
    # Add server socket object to the list of readable connections
    MATCH.append(server_socket)
 
    print ("Bind done, waiting connections in "+HOST+"::"+PORT);
 
    # Main game
    while 1:

        # Get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(MATCH,[],[],0)
        
        for sock in ready_to_read:
            # A new connection request recieved
            if sock == server_socket: 
                # Accept the connection
                sockfd, addr = server_socket.accept();
                # If socket_list already have 2 players
                if(len(socket_list) != 3):
                    MATCH.append(sockfd);
                # Print on the server who connected
                print ("Player (%s, %s) connected" % addr);
                # Append in socket_list connecteds
                socket_list.append(sock);
                server__match_send(server_socket, sockfd, "[Adversario] entrou no seu jogo\n");
                # If have two players
                if(len(MATCH) == 3):
                    startGame = True;
                    server__match_send(server_socket, server_socket, "\n\nO jogo iniciou\n");
                    MATCH[1].send("[SERVER] You are the \'X\'\n");
                    MATCH[2].send("[SERVER] You are the \'O\'\n");
                    # Get random number to decides who will start
                    randomNumber = random.randrange(2000);
                    turn = randomNumber%2;
                    # Tell who starts
                    if(turn == 0):
                        MATCH[1].send("[SERVER] You are first\n");
                        MATCH[1].send("Tutorial:\n"+printBoard(boardTutorial)+"Mesa atual:\n"+printBoard(boardContent)+"\nSua jogada:\n");
                        MATCH[2].send("[SERVER] You are second\n\n");
                    else:
                        MATCH[1].send("[SERVER] You are second\n");
                        MATCH[2].send("[SERVER] You are first\n\n");
                        MATCH[2].send("Tutorial:\n"+printBoard(boardTutorial)+"Mesa atual:\n"+printBoard(boardContent)+"\nSua jogada:\n");



            # Receive a message from a client, not a new connection
            else:
                while startGame:
                    # Process data recieved from client, 
                    try:
                        # Receiving data from the socket.
                        if (turn == 0):
                            data = MATCH[1].recv(RECV_BUFFER);
                        else:
                            data = MATCH[2].recv(RECV_BUFFER);

                        if data:
                            # There is something in the socket
                            if turn == 0:
                                # Try replace the player role
                                if(boardReplace(boardContent, int(data[0])-1, "X") == 0):
                                    startGame = False;
                                    server__match_send(server_socket,server_socket, "Jogador X foi pego trapaceando, GAME OVER\n");
                                    exit();
                                # Send the player role, and the board
                                MATCH[2].send("[Adversario] jogou: "+data[0]+"\nTutorial:\n"+printBoard(boardTutorial)+"\nMesa atual:\n"+printBoard(boardContent)+"\nSua jogada:\n");
                                MATCH[1].send(printBoard(boardContent));
                                # Check if the role results in a win
                                result, winningPath = checkWinner(boardContent, "X");
                                # If the game ends, send the winning path (or draw)
                                if result >= 0:
                                    startGame = False;
                                    server__match_send(server_socket, server_socket, winningPath);
                                    MATCH.remove(sock);
                                # Else, change the turn
                                turn = 1;
                            else:
                                if(boardReplace(boardContent, int(data[0])-1, "O") == 0):
                                    startGame = False;
                                    server__match_send(server_socket,server_socket, "Jogador O foi pego trapaceando, GAME OVER\n");
                                    exit();
                                # Send the player role, and the board
                                MATCH[1].send("[Adversario] jogou: "+data[0]+"\nTutorial:\n"+printBoard(boardTutorial)+"\nMesa atual:\n"+printBoard(boardContent)+"\nSua jogada:\n");
                                MATCH[2].send(printBoard(boardContent));
                                # Check if the role results in a win
                                result, winningPath = checkWinner(boardContent, "O");
                                # If the game ends, send the winning path (or draw)
                                if result >= 0:
                                    startGame = False;
                                    server__match_send(server_socket, server_socket, winningPath);
                                    MATCH.remove(sock);
                                # Else, change the turn
                                turn = 0;

                        else:
                            # Remove the socket that's broken    
                            if sock in MATCH:
                                MATCH.remove(sock);
                                socket_list.remove(sock);
                            # At this stage, no data means probably the connection has been broken
                            server__match_send(server_socket, sock, "Player (%s, %s) is offline\n" % addr);
                    # exception 
                    except:
                        # The players role a invalid position
                        if turn == 0:
                            MATCH[2].send("[SERVER] Jogador adversario fez uma jogada invalida, voce ganhou!\nGAME OVER\n");
                            MATCH[1].send("[SERVER] Voce fez uma jogada invalida, voce perdeu!\nGAME OVER\n");
                        else:
                            MATCH[2].send("[SERVER] Voce fez uma jogada invalida, voce perdeu!\nGAME OVER\n");
                            MATCH[1].send("[SERVER] Jogador adversario fez uma jogada invalida, voce ganhou!\nGAME OVER\n");
                        continue;

    server_socket.close();

def checkWinner(board, role):
    # Check Lines
    if (len(set([board[0], board[1], board[2], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 1|2|3\nGame Over\n\n";
    if (len(set([board[3], board[4], board[5], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 4|5|6\nGame Over\n\n";
    if (len(set([board[6], board[7], board[8], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 7|8|9\nGame Over\n\n";

    # Check Columns
    if (len(set([board[0], board[3], board[6], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 0|3|6\nGame Over\n\n";
    if (len(set([board[1], board[4], board[7], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 1|4|7\nGame Over\n\n";
    if (len(set([board[2], board[5], board[8], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 2|5|8\nGame Over\n\n";

    # Check Diagonals
    if (len(set([board[0], board[4], board[8], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 1|5|9\nGame Over\n\n";
    if (len(set([board[6], board[4], board[2], role])) == 1):
        return 1, "Jogador \'"+role+"\' venceu nas posicoes 3|5|7\nGame Over\n\n";

    # If not empty slots left, draw
    if " " not in board:
        return 0, "Jogo finalizou em empate\n\n";

    return -1, "";


def printBoard(board):
    return ("|" + board[0] + "|" + board[1]  + "|" + board[2] + "|\n" 
            + "|" + board[3] + "|" + board[4]  + "|" + board[5] + "|\n" 
            + "|" + board[6] + "|" + board[7]  + "|" + board[8] + "|\n");
    
def boardReplace(board, position, role):
    # Verify if the position is empty
    if board[position] == " ":
        board[position] = role;
        return 1;
    return 0;

# server__match_send messages to all connected clients
def server__match_send (server_socket, sock, message):
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
 
if __name__ == "__main__":

    exit(tic_tac_toe_server()) 
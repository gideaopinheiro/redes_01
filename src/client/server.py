import random
import socket
import threading
import time

symbols = ['X', 'O']
turn = 0

def listen_player(player, opponent, player_turn):
    global turn

    while True:
        msg = player[0].recv(1024).strip()
        print(player[1],'->', msg.decode())

        if msg == b'DESCONECTAR':
            player[0].send(b'DESCONECTAR')
            break

        elif player_turn == turn % 2:
            if turn == 8:
                msg = b'EMPATE:' + msg
                player[0].send(msg)
                opponent[0].send(msg)
            else:
                msg = b'VEZ:' + msg
                turn += 1
                opponent[0].send(msg)
                print(opponent[1],'<-', msg.decode())


def game(players):
    order = random.randint(0, 1)

    if order == 1: players.reverse()

    players[0][0].send(b'INICIO:X')
    players[1][0].send(b'INICIO:O')
    
    threading.Thread(target=listen_player, args=(players[0], players[1], 0)).start()
    threading.Thread(target=listen_player, args=(players[1], players[0], 1)).start()
    


def main():
    address = ("Orpheus", 6544)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(address)
    server_socket.listen(1)

    print('Server initiated!\n')
    global turn
    
    while True:
        turn = 0
        player1 = server_socket.accept()
        print("New connection to ", player1[1])
        player2 = server_socket.accept()
        print("New connection to ", player2[1])

        time.sleep(0.5)

        game([player1, player2])

    # thr = threading.Thread(target=thread_server, args=(stream, client_address,))
    # threads.append(thr)
    # thr.start()

main()
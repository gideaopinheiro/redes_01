import random
import socket
import threading

symbols = ['X', 'O']

def game(players):
    order = random.randint(0, 1)

    if order == 1: players.reverse()

    players[0][0].send(b'INICIO:X')
    players[1][0].send(b'INICIO:O')
    

    while True:
        for i in range(2):
            msg = players[i][0].recv(1024)
            print(players[i][1],'->', msg)

            msg = b'VEZ:' + msg
            players[i-1][0].send(msg)
            print(players[i-1][1], '<-', msg)
    


def main():
    address = ("localhost", 20001)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(address)
    server_socket.listen(1)

    print('Server initiated!\n')

    player1 = server_socket.accept()
    print("New connection to ", player1[1])
    player2 = server_socket.accept()
    print("New connection to ", player2[1])

    game([player1, player2])

    # thr = threading.Thread(target=thread_server, args=(stream, client_address,))
    # threads.append(thr)
    # thr.start()

main()
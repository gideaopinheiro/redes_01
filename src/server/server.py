# Rebece uma mensagem
# Valida a mensagem mensagem
# Processa a mensagem
# Devolve uma resposta

from socket import *
import threading
from collections import deque

from app.Player import Player           
from app.Board import Board


address = ('localhost', 20001)

server = socket(AF_INET, SOCK_STREAM)
server.bind(address)
server.listen(5)

games = {}
waiting_list = []
waiting_clients = []
character_options = deque(['X', 'O'])


def turn_off(client, msg='DESCONECTAR'):
  client.send(msg.encode())
  client.shutdown(SHUT_WR)
  client.close()


def on_new_player(socket_client, client_id, board):
  while True:
    msg = socket_client.recv(1024)
    msg = msg.decode()

    if msg == 'DESCONECTAR':
      turn_off(socket_client, msg)
      break

    x, rest = msg.split('#')
    y, char = rest.split(':')

    movement_return = board.make_a_move(int(x), int(y), char, client_id)


def initiate_game():
  global character_options

  while True:
    con, addr = server.accept()

    if len(character_options) == 0:
      character_options.append('X')
      character_options.append('O')

    global waiting_list
    global waiting_clients

    board = None
    _, player_id = con.getpeername()

    waiting_clients.append(con)
    player = Player(player_id, character_options.popleft(), con)

    waiting_list.append(player)

    if len(waiting_list) % 2 == 0:
      board = Board(waiting_list[0], waiting_list[1])
      for cli in range(len(waiting_clients)):
        message = f'INICIO:{waiting_list[cli].character}'
        waiting_clients[cli].send(message.encode())
        threading.Thread(target=on_new_player, args=(waiting_clients[cli], waiting_list[cli].id, board)).start()


initiate_game()
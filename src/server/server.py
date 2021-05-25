# Rebece uma mensagem
# Valida a mensagem mensagem
# Processa a mensagem
# Devolve uma resposta

from socket import *
import threading
from collections import deque

from app.Player import Player           
from app.Board import Board


host = gethostname()
port = 6544
print(f'host: {host}\nport: {port}')

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(5)

games = {}
waiting_list = []
waiting_clients = []
character_options = deque(['X', 'O'])


def on_new_player(client, board):
  # global waiting_list
  # global character_options
  # global waiting_clients
  # board = None
  # _, player_id = client.getpeername()

  # waiting_clients.append(client)
  # player = Player(player_id, character_options.popleft())

  # waiting_list.append(player)

  # if len(waiting_list) % 2 == 0:
  #   print(len(waiting_list))
  #   board = Board(waiting_list[0], waiting_list[1])
    # waiting_list.clear()
    # for cli in waiting_clients:
  while True:
    msg = client.recv(1024)
    msg = msg.decode()
    # N#N:C
    if msg == 'sair':
      break
    x, rest = msg.split('#')
    y, char = rest.split(':')
    movement_return = board.make_a_move(int(x), int(y), char)
    print(msg)
    print(movement_return)


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
    player = Player(player_id, character_options.popleft())

    waiting_list.append(player)

    if len(waiting_list) % 2 == 0:
      board = Board(waiting_list[0], waiting_list[1])
      for cli in waiting_clients:
        threading.Thread(target=on_new_player, args=(cli, board)).start()


initiate_game()
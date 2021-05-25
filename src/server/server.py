# Rebece uma mensagem
# Valida a mensagem mensagem
# Processa a mensagem
# Devolve uma resposta

from socket import *

host = gethostname()
port = 6543
print(f'host: {host}\nport: {port}')

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(5)

while True:
  con, addr = server.accept()
  msg = con.recv(1024)
  msg = msg.decode()
  print(msg)
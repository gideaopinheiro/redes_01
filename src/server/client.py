from socket import *

address = ('localhost', 20001)

client = socket(AF_INET, SOCK_STREAM)
client.connect(address)

while True:
  msg = client.recv(1024)
  msg = msg.decode()
  print(msg)
  msg = input('escreva uma mensagem: ')
  if msg == 'sair':
    break
  client.send(msg.encode())
  
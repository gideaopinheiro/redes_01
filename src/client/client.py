from socket import *

host = gethostname()
port = 6544

client = socket(AF_INET, SOCK_STREAM)
client.connect((host, port))

while True:
  msg = input('envie uma mensagem: ')
  if msg == 'close':
    break
  client.send(msg.encode())
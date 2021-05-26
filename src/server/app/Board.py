class Player:
  def __init__(self, id, character):
    self.id = id
    self.character = character

class Board:
  def __init__(self, player1: Player, player2: Player):
    self.board = [
      ["", "", ""],
      ["", "", ""],
      ["", "", ""]
      ]
    self.players = {player1.character: player1, player2.character: player2}
    self.status = 'Ninguem venceu'
    self.player_time = player1

  
  def make_a_move(self, x, y, char, client_id):
    if self.__validate_move(x, y, char)[0] and client_id == self.player_time.id and self.players[char].id == self.player_time.id:
      print('validou')
      
      self.board[x][y] = char
      self.player_time = self.players['X'] if char == 'O' else self.players['O']
      status, obj = self.checkGameStatus()
      
      if status == 'venceu':
        message_winner = f'VENCEU'
        message_loser = f'PERDEU'
        obj['winner'].send(message_winner.encode())
        obj['loser'].send(message_loser.encode())
        return True
      
      elif status == 'empatou':
        message = 'EMPATOU'
        self.players['X'].client.send(message.encode())
        self.players['O'].client.send(message.encode())
        return True
      
      else:
        message = f'VEZ:{x}#{y}:{char}'
        self.player_time.client.send(message.encode())
        return True
    
    return False


  def __validate_move(self, x, y, char):
    if x >= 0 and x <= 2 and y >= 0 and y <= 3:
      if self.board[x][y] == "":
        return True, 'Campo valido'
      return False, 'Campo preenchido'
    return False, 'Fora dos limites do board'


  def __is_completed(self) -> bool:
    for i in range(0, 3):
      for j in range(0, 3):
        if self.board[i][j] == "":
          return False
    return True


  def checkGameStatus(self):
    for i in range(0, 3):
      if (self.board[i][0] == self.board[i][1] == self.board[i][2]) and (self.board[i][0] == 'X'):
        return 'venceu', {'winner': self.players['X'].client, 'loser': self.players['O'].client}

      elif (self.board[i][0] == self.board[i][1] == self.board[i][2]) and (self.board[i][0] == 'O'):
        return 'venceu', {'winner': self.players['O'].client, 'loser': self.players['X'].client}

      elif (self.board[0][i] == self.board[1][i] == self.board[2][i]) and (self.board[0][i] == 'X'):
        return 'venceu', {'winner': self.players['X'].client, 'loser': self.players['O'].client}

      elif (self.board[0][i] == self.board[1][i] == self.board[2][i]) and (self.board[0][i] == 'O'):
        return 'venceu', {'winner': self.players['O'].client, 'loser': self.players['X'].client}

    if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] == 'X'):
        return 'venceu', {'winner': self.players['X'].client, 'loser': self.players['O'].client}

    elif (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] == 'O'):
        return 'venceu', {'winner': self.players['O'].client, 'loser': self.players['X'].client}

    elif (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] == 'X'):
        return 'venceu', {'winner': self.players['X'].client, 'loser': self.players['O'].client}

    elif (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] == 'O'):
        return 'venceu', {'winner': self.players['O'].client, 'loser': self.players['X'].client}

    if self.__is_completed():
       return 'empatou', {}
       
    else:
       return 'jogando', {}
    
      




# board = Board(Player('abc', 'X'), Player('rkt', 'O'))
# print(board.make_a_move(0, 0, 'X'))
# # print(board.make_a_move(0, 0, 'X'))



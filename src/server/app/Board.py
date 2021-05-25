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
    self.players = {player1.character: player1.id, player2.character: player2.id}
    self.status = 'Ninguem venceu'
  
  def make_a_move(self, x, y, char):
    if self.__validate_move(x, y, char)[0]:
      self.board[x][y] = char
      return "Movimento completado"
    return "Movimento não aceito"

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

  def checkGameStatus(self) -> str:
    for i in range(0, 3):
      if (self.board[i][0] == self.board[i][1] == self.board[i][2]) and (self.board[i][0] == 'X' or self.board[i][0] == 'O'):
        return 'venceu'
      elif (self.board[0][i] == self.board[1][i] == self.board[2][i]) and (self.board[0][i] == 'X' or self.board[0][i] == 'O'):
        return 'venceu'
    if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] == 'X' or self.board[0][0] == 'O'):
      return 'venceu'
    elif (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] == 'X' or self.board[0][2] == 'O'):
      return 'venceu'
    if self.__is_completed():
       return 'empatou'
    else:
       return 'ainda não acabou'
    
      




# board = Board(Player('abc', 'X'), Player('rkt', 'O'))
# print(board.make_a_move(0, 0, 'X'))
# # print(board.make_a_move(0, 0, 'X'))



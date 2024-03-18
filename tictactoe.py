import numpy as np

class TicTacToe:

  # We initialise a 3x3 board with zeros indicating available positions
  # and update positions with 1 if player 1 takes a move and -1 if player 2 takes a move.
  def __init__(self, p1, p2):
    self.board = np.zeros((3, 3))
    self.p1 = p1
    self.p2 = p2

    self.moves = []  # List of player moves (positions) in order
    self.isEnd = False
    self.boardHash = None
    self.playerSymbol = 1  # Player 1 will play first, toggled after every move

  # Get a unique hash of the current board state
  # If nextPos is provided, we compute the hash including that position
  def getHash(self, nextPos=None):
    if nextPos:
      assert self.board[nextPos] == 0
      board = self.board.copy()
      board[nextPos] = self.playerSymbol
      return str(board.reshape(3*3))
    else: 
      self.boardHash = str(self.board.reshape(3*3))
      return self.boardHash

  def availablePositions(self):
    available = []
    for i in range(3):
      for j in range(3):
        if self.board[i][j] == 0:
          available.append((i, j))
    return available

  def playGame(self, verbose=False):
    assert not self.isEnd
    while not self.isEnd:
      self.playNextMove()
      if verbose:
        self.printBoard()
      winner = self.winner()
      if winner is not None:
        self.giveReward(winner)
        return winner

  def playNextMove(self):
    assert self.isEnd == False and len(self.availablePositions()) > 0
    if self.playerSymbol == 1:
      position = self.p1.nextMove(self)
    else:
      position = self.p2.nextMove(self)
    self.updateState(position)

  def updateState(self, position):
    assert self.board[position] == 0
    self.board[position] = self.playerSymbol
    self.playerSymbol *= -1
    self.moves.append(self.getHash())

  def printBoard(self):
    symbol = { 0: ' ', 1: 'X', -1: 'O' }
    board = self.board
    print("")
    print(" " + " | ".join(symbol[val] for val in self.board[0]))
    print("-----------")
    print(" " + " | ".join(symbol[val] for val in self.board[1]))
    print("-----------")
    print(" " + " | ".join(symbol[val] for val in self.board[2]))
    print("")

  def winner(self):
    positions = [
      # Rows
      [(0,0), (0,1), (0,2)],
      [(1,0), (1,1), (1,2)],
      [(2,0), (2,1), (2,2)],
      # Columns
      [(0,0), (1,0), (2,0)],
      [(0,1), (1,1), (2,1)],
      [(0,2), (1,2), (2,2)],
      # Diagonals
      [(0,0), (1,1), (2,2)],
      [(0,2), (1,1), (2,0)],
    ]

    # See if there is a winner
    for parr in positions:
      cum = sum([self.board[parr[i]] for i in range(3)])
      if cum == 3 or cum == -3:
        self.isEnd = True
        return 1 if cum == 3 else -1

    # If it's a tie
    if len(self.availablePositions()) == 0:
      self.isEnd = True
      return 0

    return None


  # RL reward at end of game
  def giveReward(self, winner):
    assert winner != None

    if winner == 1:
      self.p1.feedReward(1.0, self.moves)
      self.p2.feedReward(0.0, self.moves)
    elif winner == -1:
      self.p1.feedReward(0.0, self.moves)
      self.p2.feedReward(1.0, self.moves)
    elif winner == 0:
      self.p1.feedReward(0.2, self.moves)
      self.p2.feedReward(0.5, self.moves)


####################################

# ttt = TicTacToe('P1', 'P2')

# ttt.updateState((0, 0))
# ttt.updateState((0, 2))
# ttt.updateState((1, 1))
# ttt.updateState((1, 2))
# ttt.updateState((2, 0))
# ttt.updateState((2, 2))

# ttt.printBoard()
# print(ttt.winner())

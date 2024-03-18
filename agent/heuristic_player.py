import random

class HeuristicPlayer:
  def __init__(self, playerSymbol):
    self.playerSymbol = playerSymbol

  def nextMove(self, ttt):
    available = ttt.availablePositions()
    assert(len(available) > 0)

    # Neither we, nor the opponent, can win immediately
    if len(available) >= 7:
      return available[random.randrange(len(available))]

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

    # See if we can win immediately
    for parr in positions:
      cum = sum([ttt.board[parr[i]] for i in range(3)])
      # If we have 2 of the 3 slots and the third is empty, we can win
      if cum == 2*self.playerSymbol:
        return next(pos for pos in parr if ttt.board[pos] == 0)

    # If opponent can win immediately, block them
    for parr in positions:
      cum = sum([ttt.board[parr[i]] for i in range(3)])
      # If we have 2 of the 3 slots and the third is empty, we can win
      if cum == -2*self.playerSymbol:
        return next(pos for pos in parr if ttt.board[pos] == 0)

    # Else, just play a random move
    idx = random.randrange(len(available))
    return available[idx]

  def feedReward(self, winner, moves):
    pass

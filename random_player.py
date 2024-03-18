import random

class RandomPlayer:
  def __init__(self, playerSymbol):
    self.playerSymbol = playerSymbol

  def nextMove(self, ttt):
    available = ttt.availablePositions()
    assert(len(available) > 0)
    idx = random.randrange(len(available))
    return available[idx]

  def feedReward(self, winner, moves):
    pass

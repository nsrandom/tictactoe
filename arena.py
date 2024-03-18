from tictactoe import TicTacToe
from random_player import RandomPlayer
from heuristic_player import HeuristicPlayer
from rl_player import RLPlayer

class Arena():
  """Arena for different TicTacToe strategies to compete against each other"""
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
    # Counts of wins and ties
    self.p1_wins = 0
    self.p2_wins = 0
    self.ties = 0
    # Cumulative count of wins and ties
    self.p1_wins_cum = []
    self.p2_wins_cum = []
    self.ties_cum = []

  def update_stats(self, winner):
    if winner == 1:
      self.p1_wins += 1
    elif winner == -1:
      self.p2_wins += 1
    else:
      self.ties += 1

    self.p1_wins_cum.append(1 if winner == 1 else 0)
    self.p2_wins_cum.append(1 if winner == -1 else 0)
    self.ties_cum.append(1 if winner == 0 else 0)

  def fight(self, iterations, skip=0):
    for n in range(iterations):
      ttt = TicTacToe(self.p1, self.p2)
      winner = ttt.playGame()

      # Ignore the first `skip` runs from stats
      if n >= skip:
        self.update_stats(winner)

    return (self.p1_wins, self.p2_wins, self.ties)

  def fightVerbose(self):
    ttt = TicTacToe(self.p1, self.p2)
    winner = ttt.playGame(verbose=True)

  def last_n_stats(self, n):
    assert(n <= len(self.p1_wins_cum))
    p1_wins = sum(self.p1_wins_cum[-n:])
    p2_wins = sum(self.p2_wins_cum[-n:])
    ties    = sum(self.ties_cum[-n:])
    return (p1_wins, p2_wins, ties)

#######################################################

# Random vs Random player
#   p1 wins 58%, p2 wins 29%, 13% are ties
# p1 = RandomPlayer(playerSymbol=1)
# p2 = RandomPlayer(playerSymbol=-1)

# Heuristic vs Heuristic player
#   p1 wins 31%, p2 wins 17%, 52% are ties
# p1 = HeuristicPlayer(playerSymbol=1)
# p2 = HeuristicPlayer(playerSymbol=-1)

# Random vs Heuristic player
#   p1 wins 6.5%, p2 wins 69%, 24.5% are ties
# p1 = RandomPlayer(playerSymbol=1)
# p2 = HeuristicPlayer(playerSymbol=-1)

# Heuristic vs Random player
#   p1 wins 89.5%, p2 wins 1.2%, 9.3% are ties
# p1 = HeuristicPlayer(playerSymbol=1)
# p2 = RandomPlayer(playerSymbol=-1)

# Random vs ReinforcementLearning player
#   p1 wins 6.5%, p2 wins 69%, 24.5% are ties
# p1 = RandomPlayer(playerSymbol=1)
# p2 = RLPlayer(playerSymbol=-1)
# p2 = RLPlayer(playerSymbol=-1, verbose=True)

# Heuristic vs ReinforcementLearning player
# p1 = HeuristicPlayer(playerSymbol=1)
# p2 = RLPlayer(playerSymbol=-1)

# ReinforcementLearning vs ReinforcementLearning player
p1 = RLPlayer(playerSymbol=1)
p2 = RLPlayer(playerSymbol=-1)

arena = Arena(p1, p2)
# arena.fightVerbose()

(p1_wins, p2_wins, ties) = arena.fight(iterations=10000)
p2.savePlayerModel()

total = p1_wins + p2_wins + ties
print(f"Cumulative: ({total})")
print(f"  P1 wins: {p1_wins/total*100: .2f}%")
print(f"  P2 wins: {p2_wins/total*100: .2f}%")
print(f"  Ties: {ties/total*100: .2f}%")

total = 1000
(p1_wins, p2_wins, ties) = arena.last_n_stats(n=total)
print(f"In last {total} iterations:")
print(f"  P1 wins: {p1_wins/total*100: .2f}%")
print(f"  P2 wins: {p2_wins/total*100: .2f}%")
print(f"  Ties: {ties/total*100: .2f}%")

print(len(p2.state_values.keys()))

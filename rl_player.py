import numpy as np
import pickle

FILENAME = 'rlplayer.pickle'

class RLPlayer:

  # exp_rate: % of times the player will choose an exploratory option, 
  #   instead of the current best estimate
  def __init__(self, playerSymbol, exp_rate=0.3, verbose=False):
    self.playerSymbol = playerSymbol
    self.exp_rate = exp_rate
    self.state_values = {}
    self.lr = 0.2
    self.decay_gamma = 0.9
    self.verbose = verbose
    # Load previously stored state values
    try:
      file = open(FILENAME, 'rb')
      self.state_values = pickle.load(file)
      file.close()
    except Exception:
      pass

  def savePlayerModel(self):
    try:
      file = open(FILENAME, 'wb')
      pickle.dump(self.state_values, file)
      file.close()
    except Exception:
      pass

  def nextMove(self, ttt):
    positions = ttt.availablePositions()
    if np.random.uniform(0, 1) <= self.exp_rate:
      idx = np.random.choice(len(positions))
      action = positions[idx]
    else:
      # Choose the position with the highest state value
      # value will be zero if we haven't seen this state before
      value_max = -1000
      action = None
      for pos in positions:
        next_hash = ttt.getHash(nextPos=pos)
        value = 0 if self.state_values.get(next_hash) is None else self.state_values[next_hash]
        if value >= value_max:
          value_max = value
          action = pos

    return action


  def feedReward(self, reward, moves):
    # Reverse iterate the moves (positions/states) that were played and update the values
    # of previous states for this player
    for state in reversed(moves):
      if self.state_values.get(state) is None:
        self.state_values[state] = 0

      # Using Value iteration from RL
      #   The updated value of state t equals the current value of state t 
      #   adding the difference between the value of next state and the value of current state,
      #   which is multiplied by a learning rate α (Given the reward of intermediate state is 0).
      self.state_values[state] += self.lr * (self.decay_gamma * reward - self.state_values[state])
      reward = self.state_values[state]

      if self.verbose:
        print(f"{state} => {self.state_values[state]}")



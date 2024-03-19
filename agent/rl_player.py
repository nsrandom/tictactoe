import numpy as np
import pickle

# A common store to share the learned state-value data across RLPlayer agents
class RLStore:
  def __init__(self, filename):
    self.filename = filename
    # Load previously stored state values
    try:
      file = open(filename, 'rb')
      self.state_values = pickle.load(file)
      file.close()
    except Exception:
      self.state_values = {}

  def save(self):
    try:
      file = open(self.filename, 'wb')
      pickle.dump(self.state_values, file)
      file.close()
    except Exception:
      pass

P1_STORE = RLStore(filename='rlplayer1.pickle')
P2_STORE = RLStore(filename='rlplayer2.pickle')

class RLPlayer:
  # exp_rate: % of times the player will choose an exploratory option, 
  #   instead of the current best estimate
  def __init__(self, playerSymbol, exp_rate=0.3, verbose=False):
    self.name = "RL Player"
    self.playerSymbol = playerSymbol
    self.exp_rate = exp_rate
    self.lr = 0.2
    self.decay_gamma = 0.9
    self.verbose = verbose
    self.store = P1_STORE if playerSymbol == 1 else P2_STORE

  def savePlayerModel(self):
    self.store.save()

  def nextMove(self, ttt):
    positions = ttt.availablePositions()
    if np.random.uniform(0, 1) <= self.exp_rate:
      idx = np.random.choice(len(positions))
      return positions[idx]

    # Else, Choose the position with the highest state value
    # value will be zero if we haven't seen this state before
    value_max = -1000
    action = None
    state_values = self.store.state_values
    for pos in positions:
      next_hash = ttt.getHash(nextPos=pos)
      value = 0 if state_values.get(next_hash) is None else state_values[next_hash]
      if value >= value_max:
        value_max = value
        action = pos
    return action


  def feedReward(self, reward, moves):
    state_values = self.store.state_values
    # Reverse iterate the moves (positions/states) that were played and update the values
    # of previous states for this player
    for state in reversed(moves):
      if state_values.get(state) is None:
        state_values[state] = 0

      # Using Value iteration from RL
      #   The updated value of state t equals the current value of state t 
      #   adding the difference between the value of next state and the value of current state,
      #   which is multiplied by a learning rate α (Given the reward of intermediate state is 0).
      state_values[state] += self.lr * (self.decay_gamma * reward - state_values[state])
      reward = state_values[state]

      if self.verbose:
        print(f"{state} => {state_values[state]}")



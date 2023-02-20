import random
import numpy as np
class User:
  def __init__(self, name):
    self.name = name
    self.ID = int(np.random.normal(0, 1, 1)[0] * 10000)
    # self.connection = 
    self.queue = []
    self.active = True
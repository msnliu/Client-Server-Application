import random
import numpy as np
class User:
  def __init__(self, name):
    self.name = name
    self.ID = name + str(np.random.randint(0, 10000))
    # self.connection = 
    self.queue = []
    self.active = True
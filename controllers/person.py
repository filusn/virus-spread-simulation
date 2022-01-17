import random
from typing import Tuple


class Person:
  def __init__(self, map_size: Tuple[int, int], walking_range: Tuple[float, float] = [-0.5, 0.5],
               incubation_period: int = 3, illness_period: int = 10,
               death_prob: int = 0.05, self_isolation: bool = False):
    self.incubation_period = incubation_period
    self.illness_period = int(random.gauss(illness_period, 2)) # Random illness period with Gaussian distribution mu=illness_period, sigma=2
    self.walking_range = walking_range
    self.map_size = map_size
    self.death_prob = death_prob
    self.self_isolation = self_isolation # Chance that infected/ill person will isolate himself with probability of p=0.1
    self.isolated = False

    self.position = [random.uniform(0, self.map_size[0]), random.uniform(0, self.map_size[1])]

    self.status = 0
    self.status_time = 0

  def move(self) -> None:
    dx = random.uniform(self.walking_range[0], self.walking_range[1])
    dy = random.uniform(self.walking_range[0], self.walking_range[1])

    self.position[0] += dx
    self.position[1] += dy

    if self.position[0] > self.map_size[0]:
      self.position[0] = self.map_size[0] - (self.position[0] - self.map_size[0])

    if self.position[1] > self.map_size[1]:
      self.position[1] = self.map_size[1] - (self.position[1] - self.map_size[1])

  def self_isolate(self) -> None:
    # Check randomly with the probability of 0.1 if the person notice 
    # the symptoms and self isolates himself.
    if random.random() <= 0.1:
      self.isolated = True

  def update_status(self) -> None:
    if self.status == 1:
      if self.status_time == self.incubation_period:
        self.status = 2
        self.status_time = 0
      else:
        self.status_time += 1
    elif self.status == 2:
      if self.status_time == self.illness_period:
        self.status = 3
        self.status_time = 0
        self.isolated = False
        self.check_survival()
      else:
        self.status_time += 1
    elif self.status == 1:
      self.status_time += 1

  def check_survival(self) -> None:
    if random.random() <= self.death_prob:
      self.status = 4

  def update(self) -> None:
    self.move()
    self.update_status()
    
    if self.self_isolation and not self.isolated:
      self.self_isolate()
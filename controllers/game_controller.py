import math
import random
from typing import Optional, Tuple, List
from controllers import Person


class Controller:
  def __init__(self, pop_num: int = 100, map_size: Tuple[int, int] = (100, 100),
               init_infected: int = 1, infection_dist: int = 1,
               infection_prob: int = 0.5, death_prob: int = 0.05,
               walking_range: Tuple[int, int] = (-0.1, 0.1),
               incubation_period: int = 3, illness_period: int = 10,
               self_isolation: bool = False, lockdown: Optional[Tuple[int, int]] = None) -> None:
    self.pop_num = pop_num
    self.map_size = map_size
    self.init_infected = init_infected
    self.infection_dist = infection_dist
    self.infection_prob = infection_prob
    self.death_prob = death_prob
    self.walking_range = walking_range
    self.incubation_period = incubation_period
    self.illness_period = illness_period
    self.self_isolation = self_isolation
    self.population = self._create_population()
    if lockdown:
      self.lockdown = lockdown
    self.step_number = 0

    self.stats = {
        'pos_x': [],
        'pos_y': [],
        'status': [],
        '0': [],
        '1': [],
        '2': [],
        '3': [],
        '4': []
    }

    self.update_stats()

  def _create_population(self) -> List[Person]:
     population = [Person(walking_range=self.walking_range, map_size=self.map_size) for person in range(self.pop_num)]
     for person in population[:self.init_infected]:
       person.status = 2
    
     return population

  def _transmit_disease(self, carrier: Person) -> None:
    for person in self.population:
      if person is carrier or person.status != 0:
        continue

      dist = self._calculate_distance(carrier, person)
      chance = random.random()
      if dist <= self.infection_dist and chance <= self.infection_prob:
        person.status = 1
        person.status_time = 0
        
  def _calculate_distance(self, per1: Person, per2: Person) -> float:
    return math.sqrt((per1.position[0] - per2.position[0]) ** 2 + (per1.position[1] - per2.position[1]) ** 2)

  def simulate(self, steps):
    for step_no in range(steps):
      carriers = [person for person in self.population if person.status == 2 and not person.isolated]
      for carrier in carriers:
        self._transmit_disease(carrier)

      for person in self.population:
        if person.status != 4:
          person.update()

      self.update_stats()
      self.step_number += 1

  def update_stats(self) -> None:
    self.stats['pos_x'].append([person.position[0] for person in self.population])
    self.stats['pos_y'].append([person.position[1] for person in self.population])
    self.stats['status'].append([person.status for person in self.population])

    for status in range(5):
      self.stats[str(status)].append(len([person for person in self.population if person.status == status]))

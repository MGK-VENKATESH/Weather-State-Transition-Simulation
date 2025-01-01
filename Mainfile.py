import numpy as np

class WeatherSimulation:
   def __init__(self, transition_probabilities, holding_times):
      self.trans_prob = transition_probabilities
      self.h_times = holding_times
      self.sts = list(transition_probabilities.keys())
      self.curr_st = 'sunny'
      self.rmng_hrs = self.h_times[self.curr_st]
      tolerance = 1e-7
      for state, transitions in transition_probabilities.items():
         total_prob = sum(transitions.values())
         if abs(total_prob - 1) > tolerance:
            raise RuntimeError(f"The sum of transition probabilities for state {state} should equal 1 but it is not satisfied.")

   def get_states(self):
      return self.sts
   
   
   def current_state(self):
      return self.curr_st
   
   def update_state(self):
      transitions = self.trans_prob[self.curr_st]
      next_state = np.random.choice(self.sts, p=list(transitions.values()))
      self.curr_st = next_state
      self.rmng_hrs = self.h_times[next_state]
            
   def next_state(self):
      self.rmng_hrs -= 1
      if self.rmng_hrs == 0:
         self.update_state()
         
         
   def set_state(self, new_state):
      if new_state not in self.sts:
         raise ValueError(f"This new state :'{new_state}' is not a valid state.It is not presented in states")
      self.curr_st = new_state
      self.rmng_hrs = self.h_times[new_state]
      
      
   def current_state_remaining_hours(self):
      return self.rmng_hrs
   
   
   def iterable(self):
      while True:
         yield self.curr_st
         self.next_state()
         
         
   def simulate(self, hours):
      st_counts = {}
      for state in self.sts:
         st_counts[state] = 0

      for _ in range(hours):
         st_counts[self.curr_st] += 1
         self.next_state()
      total_counts = sum(st_counts.values())
      
      
      st_percentages = []
      for state in self.sts:
         percentage = (st_counts[state] / total_counts) * 100
         st_percentages.append(percentage)
      return st_percentages
   
   



my_transitions = {
   'sunny': {'sunny': 0.7, 'cloudy': 0.3, 'rainy': 0, 'snowy': 0},
    'cloudy': {'sunny': 0.5, 'cloudy': 0.3, 'rainy': 0.15, 'snowy': 0.05},
    'rainy': {'sunny': 0.6, 'cloudy': 0.2, 'rainy': 0.15, 'snowy': 0.05},
    'snowy': {'sunny': 0.7, 'cloudy': 0.1, 'rainy': 0.05, 'snowy': 0.15}
 }
 my_holding_times = {'sunny': 1, 'cloudy': 2, 'rainy': 2, 'snowy': 1}


 weather_sim = WeatherSimulation(my_transitions, my_holding_times)
 weather_iter = weather_sim.iterable()
 for _ in range(5):
    print(next(weather_iter))

 print(weather_sim.simulate(10000))

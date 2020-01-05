from source.direction import *

class Game:
    def __init__(self, _map):
        self.map = _map
        
        self.current_state = None
        self.current_reward = None
        
        self.R = 100
        self.C = -2
        self.L = -20
        
        self.reset()
        
        
      
        
    def reset(self):
        self.current_state = self.map.start_point
        self.current_reward = 0
        return self.current_state.id, self.current_state
    
    def step(self, action):
        """
        param:
            action -> game state will change based on this action
            
        outputs:
            s_ -> game state after applying the action
            reward -> it's so obvious :)
            done -> terminal state is reached
        """
        action = Direction(action)
        assert isinstance(action, Direction)

        next_state = self.map.getNextCell(self.current_state, action) 
        
        if next_state is None:
            next_state = self.current_state
        else:
            self.current_state = next_state
            
        if next_state.getKey() == self.map.end_point.getKey():
            return next_state.id, self.R, True , next_state
        
        reward = 0
        
        if next_state.getType() == '2':
            reward = self.L
        elif next_state.getType() == '0' or next_state.getType() == '1':
            reward = self.C
            
        return next_state.id, reward, False , next_state
        
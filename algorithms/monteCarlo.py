import numpy as np
from source.map import CellType
from source.direction import Direction
from collections import defaultdict

class MonteCarlo:
    def __init__(self, _game):
        self.game = _game
        
        self.alpha = 0.2
        self.gamma = 0.9
        self.beta = 1.0
        self.beta_factor = 0.01
        self.epsilon = 0.2
        self.max_steps = 100
        
        self.episodes = 3000
        self.n_states = self.game.map.n_states
        self.n_actions = self.game.map.n_actions
        
        self.P = 0
        
    def initQ(self, s, a, types="ones"):
        if types == "ones":
            return np.ones((s, a))
        elif types == "random":
            return np.random.random((s, a))
        elif types == "zeros":
            return np.zeros((s, a))
    
    def softmax(self, x):
        return np.exp((self.beta + self.beta_factor)*x)
     
    def select_action(self, Q, s):
        p = np.array([self.softmax(Q[s][a]) for a in range(4)])
        # print(p.shape)
        return np.argmax(p)
    
       
    def epsilon_greedy(self, Q, s, train=False):
        if train or np.random.rand() < self.epsilon:
            action = np.argmax(Q[s, :]) # exploitation
        else:
            action = np.random.randint(0, self.n_actions) # exploration
        return action
     
    
    def generateEpisode(self, Q):
        episode = []
        state, _ = self.game.reset()
        t = 0
        
        while t < self.max_steps:
            action = self.epsilon_greedy(Q, state)
            next_state, reward, done, _ = self.game.step(action)
            t += 1
            episode.append((state, action, reward))
            if done:
                print(f"This episode took {t} timesteps")
                break
            state = next_state
        return episode
       
    def run(self):
        
        Q = self.initQ(self.n_states, self.n_actions, types="random")
        timestep_reward = []
        
        returns_sum = defaultdict(float)
        returns_count = defaultdict(float)
        
        for episode in range(self.episodes):
            print(f"Episode: {episode}")
            episode = self.generateEpisode(Q)
            # print(episode)
            sa_in_episode = set([(x[0], x[1]) for x in episode])
            
            
            total_reward = 0
            for state, action in sa_in_episode:
                sa_pair = (state, action)
                
                first_occurence_idx = next(i for i, x in enumerate(episode) if x[0] == state and x[1] == action)
                
                G = sum([x[2] * (self.gamma**i) for i, x in enumerate(episode[first_occurence_idx:])])
                
                returns_sum[sa_pair] += G
                returns_count[sa_pair] += 1.0
                Q[state][action] = returns_sum[sa_pair] / returns_count[sa_pair]                
                
                
        self.test_agent(Q, 4)
                
    def test_agent(self, Q, n_actions, delay=1):
        import time
        print("--------------------Test--------------------")
        s, state = self.game.reset()
        done = False
        epsilon = 0
        step = 1
        while True:
            time.sleep(delay)
            # env.render()
            a = np.argmax(Q[s])
            action = Direction(a)
            print(f"[{step}]Chose action {action} for state {state}")
            step += 1
            # s is just a number and is used when selecting action
            # state is an instance of Cell class which is used for 
            s, reward, done, state = self.game.step(a)
            if done:
                if reward > 0:
                    print("Reached goal!")
                else:
                    print("Shit! dead x_x")
                time.sleep(3)
                break
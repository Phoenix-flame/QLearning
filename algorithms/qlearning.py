import numpy as np
from source.map import CellType
from source.direction import Direction


class QLearning:
    def __init__(self, _game):
        self.game = _game
        
        self.alpha = 0.2
        self.gamma = 0.9
        self.beta = 1.0
        self.beta_factor = 0.01
        self.epsilon = 0.014
        self.max_steps = 2500
        
        self.episodes = 3000
        self.n_states = self.game.map.n_states
        self.n_actions = self.game.map.n_actions
        
        self.P = 0
        
    def initQ(self, s, a, types="random"):
        if types == "ones":
            return np.ones((s, a))
        elif types == "random":
            return np.random.random((s, a))
        elif types == "zeros":
            return np.zeros((s, a))
    
    def softmax(self, x):
        return np.exp(self.beta*x)
     
    def select_action(self, Q, s):
        p = np.array([self.softmax(Q[s][a]) for a in range(4)])
        return np.argmax(p)
    
       
    def epsilon_greedy(self, Q, epsilon, n_actions, s, train=False):
        if train or np.random.rand() < epsilon:
            action = self.select_action(Q, s)
        else:
            action = np.random.randint(0, n_actions)
        return action
        
    def run(self):
        
        Q = self.initQ(self.n_states, self.n_actions, types="random")
        timestep_reward = []
        
        for episode in range(self.episodes):
            print(f"Episode: {episode}")
            s = self.game.reset()
            a = self.epsilon_greedy(Q, self.epsilon, self.n_actions, s)
            t = 0
            total_reward = 0
            done = False
            while t < self.max_steps:
                t += 1
                s_, reward, done = self.game.step(a)
                total_reward += reward
                
                a_ = self.select_action(Q, s_)
                # a_ = self.epsilon_greedy(Q, self.epsilon, self.n_actions, s_)
                if done:
                    Q[s][a] += self.alpha * (reward - Q[s][a])
                else:
                    Q[s][a] += self.alpha * (reward + (self.gamma * Q[s_][a_]) - Q[s][a])
                s, a = s_, a_
                
                if done:
                    print(f"This episode took {t} timesteps and reward: {total_reward}")
                    timestep_reward.append(total_reward)
                    break
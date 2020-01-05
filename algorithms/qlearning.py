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
        return np.exp((self.beta)*x)
     
    def select_action(self, Q, s):
        
        best_idx = np.argmax(Q[s])
        p = np.array([self.softmax(Q[s][a]) for a in range(4)])
        p[best_idx] += (1-self.epsilon)
        # print(p.shape)
        return p / sum(p)
    
       
    def epsilon_greedy(self, Q, epsilon, n_actions, s, train=False):
        if train or np.random.rand() < epsilon:
            # action = np.argmax(Q[s, :]) # exploitation
            action = np.random.choice(4, 1, p = self.select_action(Q, s))
        else:
            action = np.random.randint(0, n_actions) # exploration
            # action = np.random.choice(4, 1, p=self.select_action(Q, s))
        return action
    
    def regret(self, n, Q, s):
        return n * Q[s][np.argmax(Q[s])] - np.sum(Q[s])    
        
    def run(self):
        
        Q = self.initQ(self.n_states, self.n_actions, types="random")
        timestep_reward = []
        
        # statistics
        reward_log = []
        regret_log = []
        
        for episode in range(self.episodes):
            print(f"Episode: {episode}")
            s, _ = self.game.reset()
            
            a = np.random.choice(4, 1, p=self.select_action(Q, s))
            
            t = 0
            total_reward = 0
            done = False
            while t < self.max_steps:
                t += 1
                # take a step
                s_, reward, done, _ = self.game.step(a)
                total_reward += reward
                

                a_ = np.random.choice(4, 1, p=self.select_action(Q, s_))
                Q[s][a] += self.alpha * (reward + (self.gamma * Q[s_][a_]) - Q[s][a])
                
                
                s = s_
                a = a_
                
                if done:
                    print(f"This episode took {t} timesteps and reward: {total_reward}")
                    timestep_reward.append(total_reward)
                    break
            reward_log.append(total_reward)
            regret_log.append(self.regret(t, Q, s))
        import matplotlib.pyplot as plt
        plt.plot(regret_log, 'r')
        # plt.show()
        plt.savefig('regret')
        self.test_agent(Q, 4)
                
    def test_agent(self, Q, n_actions, delay=0.01):
        import time
        print("--------------------Test--------------------")
        s, state = self.game.reset()
        done = False
        epsilon = 0
        step = 1
        
        
        import os
        try:
            os.remove('./optimal.policy')        
        except FileNotFoundError:
            pass
        
        
        with open('optimal.policy', 'w') as file:
            while step < self.max_steps:
                time.sleep(delay)
                # env.render()
                a = np.argmax(Q[s])
                action = Direction(a)
                print(f"[{step}]Chose action {action} for state {state}")
                file.write(f"[{step}]Chose action {action} for state {state}\n")
                
                
                step += 1
                # s is just a number and is used when selecting action
                # state is an instance of Cell class which is used for 
                s, reward, done, state = self.game.step(a)
                if done:
                    if reward > 0:
                        print("Reached goal!")
                    else:
                        print("Shit! dead x_x")
                    time.sleep(0.1)
                    break
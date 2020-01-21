import numpy as np
from source.map import CellType
from source.direction import Direction
from source.graphics import *

class QLearning:
    def __init__(self, _game):
        self.game = _game
        
        self.alpha = 0.2
        self.gamma = 0.9
        self.beta = 1.0
        self.beta_factor = 0.001
        self.epsilon = 0.2
        self.max_steps = 100
        
        self.episodes = 300
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
    
       
    def epsilon_greedy(self, Q, s, train=False):
        if train or np.random.rand() < self.epsilon:
            # action = np.argmax(Q[s, :]) # exploitation
            action = np.argmax(Q[s])
        else:
            action = np.random.choice(4, 1, p = self.select_action(Q, s)) # exploration
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
            
            a = self.epsilon_greedy(Q, s)
            
            t = 0
            total_reward = 0
            done = False
            while t < self.max_steps:
                t += 1
                # take a step
                s_, reward, done, _ = self.game.step(a)
                total_reward += reward
                

                a_ = self.epsilon_greedy(Q, s_)
                Q[s][a] += self.alpha * (reward + (self.gamma * Q[s_][a_]) - Q[s][a])
                
                
                s = s_
                a = a_
                
                if done:
                    print(f"This episode took {t} timesteps and reward: {total_reward}")
                    timestep_reward.append(total_reward)
                    break
            reward_log.append(total_reward/t)
            regret_log.append(self.regret(t, Q, s))
        import matplotlib.pyplot as plt
        plt.plot(reward_log, 'r')
        # plt.show()
        plt.savefig('reward')
        self.test_agent(Q, 4)
                
    def test_agent(self, Q, n_actions, delay=0.1):
        size = [300, 500]
        FULL_SCREEN = pg.DOUBLEBUF | pg.FULLSCREEN
        NORMAL = pg.DOUBLEBUF | pg.RESIZABLE
        pg.init()

        screen = pg.display.set_mode(size, NORMAL)
        
        
        g = Graphics(screen, {'col':self.game.map.cols, 'row':self.game.map.rows})
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
        
        exit = False
        with open('optimal.policy', 'w') as file:
            
            while not exit:
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        exit = True
                while step < self.max_steps:
                    g.drawBoard()
                    g.drawCells(self.game.map)
                    pg.display.update()
                    # pg.image.save(screen, f"{step}.png")
                    
                    time.sleep(delay)

                    a = np.argmax(Q[s])
                    action = Direction(a)
                    print(f"[{step}]Chose action {action} for state {state}")
                    file.write(f"[{step}]Chose action {action} for state {state}\n")
                    
                    
                    step += 1
                    # s is just a number and is used when selecting action
                    # state is an instance of Cell class which is used for 
                    s, reward, done, state = self.game.step(a)
                    self.game.map.cells[s].cellType = 1
                    
                    
                    
                    if done:
                        if reward > 0:
                            print("Reached goal!")
                            step = self.max_steps
                        else:
                            print("Shit! dead x_x")
                        time.sleep(0.1)
                        break
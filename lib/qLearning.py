"""
PROGRAMMER  : ANDI MUHAMMAD RIYADHUS ILMY
CREATE DATE : 2022/11/30 09:05
DESCRIPTION : A floating point model of reinforcement learning.
              - Randomized initial state of each episode
              - Uses decreasing epsilon
"""

import sys
import numpy as np
import random
import time
import math
import os

from lib import support as sp

class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()

class qrl:
    def __init__(self,
                 maze_x,
                 maze_y,
                 total_state, 
                 total_action, 
                 learning_rate, 
                 discount_factor,
                 initial_exploration_rate,
                 max_episode,
                 max_step,
                 goal_state,
                 reward_matrix,
                 ns_matrix,
                 random_pool,
                 Q_Matrix=None
                ):
        # Initialize Environment
        self.S = total_state
        self.A = total_action
        self.R = reward_matrix
        self.NS = ns_matrix
        
        # Initialize Q-Matrix
        if (Q_Matrix is None):
            self.Q = np.zeros((self.S, self.A))
        else:
            self.Q = Q_Matrix
            print('Q-Matrix initialized')
        
        # Initialize Hyparameters
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = initial_exploration_rate
        self.E = max_episode
        self.T = max_step

        # Initialize Goal
        self.goal_state = goal_state
        self.rand_pool = random_pool

        # Analytics
        self.runTime = 0
        self.state_visit_count = np.zeros(self.S)
        self.cumulative_rewards = []
        self.step_per_episode = []
        self.exploration_per_episode = []
        
    def policy_generator(self, qValue, eps_count):
        random_number = math.floor(random.random()*self.E)
        threshold = self.epsilon*(self.E - eps_count)
        if (random_number > threshold):
            # choose greedy action (exploitation)
            return np.argmax(qValue), 0
        else:
            # choose random action (exploration)
            return random.randint(0, self.A-1), 1

    def start(self):        
        # Initialize progress bar
        progress = 0
        output = f" Progress = {progress}%"
        Printer(output)
        div = self.E//100
        if(div == 0):
            div = 1
        
        # Get start time
        start_time = time.time()

        e = 0 # current episode
        while (e < self.E):
            # Print progress bar
            if (e%div)==0:
                progress +=1
                output = f" Progress = {progress}%"
                Printer(output)

            # initialize agent's initial state
            valid = False
            while(not(valid)):
                # check so initial state is never the goal state
                # s = random.randint(0, self.S-1)
                s = random.choice(self.rand_pool)
                if (s != self.goal_state):
                    valid = True

            # initialize counters
            t = 0
            cr = 0
            explore_count = 0

            # Continue episode until the agent reached the goal or the maximum step is reached
            while (s != self.goal_state) and (t < self.T):
                # Get all possible Q-values for the current state
                QValues = self.Q[s]

                # Generate an action
                a, explore_inc = self.policy_generator(QValues, e)
                explore_count += explore_inc

                # observe next state
                ns = self.NS[s][a]
                
                # observe reward
                r = self.R[s][a]
                cr += r

                # Get maximum Q-value of the next state
                maxQ = np.max(self.Q[ns])
                
                # Calculate the new Q-value
                q = self.Q[s][a]
                newQ = q + self.alpha * (r + (self.gamma*maxQ) - q)
                
                # Update Q-Matrix
                self.Q[s][a] = newQ

                # Record state visit count and move to the next state
                self.state_visit_count[s] += 1
                s = ns
                
                #increment step
                t += 1

            # Record analytics
            self.cumulative_rewards.append(cr)
            self.step_per_episode.append(t)
            self.exploration_per_episode.append(explore_count)
            
            # Increment episode 
            e += 1
            
        # Print Info
        self.runTime = time.time()-start_time
        print(f"\n Finished learning for {e} episodes")
        print(f" Runtime = {self.runTime} s")
        return None
    
    def shortest_path(self, start, quiet = True):
        goal = self.goal_state
        st = start
        total_action = 0
        list = []

        t = 0
        failure = False
        while (st != goal and t < self.T):
            Qt = self.Q[st]
            at = np.argmax(Qt)
            ns = self.NS[st][at]
            # Check if the agent is moving back
            if ((t>0) and (ns == list[t-1][0])):
                failure = True
                break
            total_action += 1
            save = [st, at, ns]
            list.append(save)
            st = ns
            t += 1

        if (t < self.T) and (failure == False):
            if (quiet==False): 
                print(f"Agent requires {total_action} step to reach S{goal:03d} from S{start:03d}")
            return True, list
        else:
            if (quiet==False): 
                print(f"Agent failed to reach S{goal:03d} from S{start:03d}")
                print(list)
            return False, list

    def shortest_path_test(self, 
                           start_list=None, 
                           quiet = True
        ):
        """
            Function perform shortest path test from every possible start-
            ing points or a set of starting point.
        """
        # Initialize return values
        passCount = 0
        failedCases = []
        recordList = []

        # Create test cases
        if (start_list):
            testCases = start_list
        else:
            testCases, GS, SSP = sp.randomize_goal(self.NS)
            testCases.remove(self.goal_state)

        # Perform test for every test case
        for startState in testCases:
            isPass, record = self.shortest_path(startState, quiet=quiet)
            if isPass:
                passCount += 1
            else:
                failedCases.append(startState)
            recordList.append(record)

        # Display status message
        if not(quiet):
            for i in range(len(testCases)):
                print(f' [Replay Memory of Test Case {i}]')
                for step in recordList[i]:
                    st, at, ns = step
                    print(f'{st:03d}|{at:02d}|{ns:03d}')
        print(f' Goal reached count: {passCount}/{len(testCases)}')

        return passCount, recordList, failedCases



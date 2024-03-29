# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    #works
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #initialise q table
        self.qTable = util.Counter()

    #works
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qTable[(state, action)]



    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        #if legalActions is an empty list, then there are no legal actions
        if (legalActions == []):
            return 0.0
        
        #find the maxActionVal
        else:
          maxActionVal = float('-inf')
          for action in legalActions:
              qVal = self.getQValue(state, action)
              if (qVal > maxActionVal):
                  maxActionVal = qVal
          return maxActionVal



        

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        #if legalActions is an empty list, then there are no legal actions
        if (legalActions == []):
            return None

        else:    
          maxActionList = []
          for action in legalActions:
              qVal = self.getQValue(state, action)
              if (qVal == self.getValue(state)):
                  maxActionList.append(action)

          if (maxActionList == []):
              return random.choice(legalActions)
          return random.choice(maxActionList)





    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        action = self.getPolicy(state)

        if (util.flipCoin(self.epsilon)):
          return random.choice(legalActions)

        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #x is just placeholder
        x = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * (reward + self.discount * self.getValue(nextState))
        self.qTable[(state, action)] = x

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action




#task 2
class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        featuresVector = self.featExtractor.getFeatures(state, action)
        w = self.getWeights()
        q = w * featuresVector
        return q
        

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"

        #initialise next max q value as negative infinity
        nextMaxQVal = float('-inf')
        nextLegalActions = self.getLegalActions(nextState)

        #if there are no next legal actions, next max q value must be zero
        if not nextLegalActions:
            nextMaxQVal = 0
        
        #if there are, find the max
        else:
          for nextAction in nextLegalActions:
              nextQvalue = self.getQValue(nextState, nextAction)
              nextMaxQVal = max(nextQvalue, nextMaxQVal)


        actionQVal = self.getQValue(state, action)

        #this is the given difference equation where (r + (gamma * nextq) - q) is the difference
        diff = (reward + self.discount * nextMaxQVal) - actionQVal
        featuresVector = self.featExtractor.getFeatures(state, action)

        #update weights
        for x in featuresVector:
            # where (r + (gamma * nextq) - q) is the difference
            self.weights[x] += self.alpha * diff * featuresVector[x]




    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass

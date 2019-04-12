# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"


	score = successorGameState.getScore()				#find the expected score of the next move

	ghostDist = manhattanDistance(newPos, newGhostStates[0].getPosition())		#find the closest ghost
	#print "ghost", distanceToGhost
	foodDist = [manhattanDistance(newPos, x) for x in newFood.asList()]	               #find the closest distances to food

	if(ghostDist > 0):					                                    #if the ghost is anywhere near shorten the score
		score= score-30.0/ghostDist			                  #my initial idea was to abstract the foodDist but that led to negative scores and loss, second thought 1/  but didnt get good scores 20 was the best one i tried

	if(len(foodDist)!=0):			                   #if there is still food in the list maximaze rhe score using shortest distance to food
		score = score+10.0/min(foodDist)			#same idea with ghost distance but this time it adds to the score, for 1 the scores where bad but 10 works better than any value i tried

        return score;

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState, agentIndex, depth) :		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:                                   #if we are at a leaf return the evaluation function for that gamestate
                return self.evaluationFunction(gameState)
            v = [None, float("-Inf")]                                   #a list that will keep the action and the numerecial value of that action
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)             #get successors
                result = minimax(currentState, agentIndex+1, depth)                     #for current game state return the minimax result of the rest of the tree(next agent)
                if type(result)==list:                                              #result could either be a list or a numerecial value of the evaluation function
                    result = result[1]
                if v[1] < result:                                               #keep the max value
                    v = [action,result]
            return v

        def min_value(gameState, agentIndex, depth) :		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:                                   #if we are at a leaf return the evaluation function for that gamestate
                return self.evaluationFunction(gameState)
            v = [None, float("Inf")]                                                #a list that will keep the action and the numerecial value of that action
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)               #get successors
                result = minimax(currentState, agentIndex+1, depth)                     #for current game state return the minimax result of the rest of the tree(next agent)
                if type(result) == list:                                                #result could either be a list or a numerecial value of the evaluation function
                    result= result[1]
                if result < v[1]:
                    v = [action,result]                                              #keep the min value
            return v

        def minimax(gameState, agentIndex, depth):

            if agentIndex == gameState.getNumAgents():      #if we searched all the agents for a certain depth go to the next and start anew
                depth = depth+1
                agentIndex = 0

            if( depth == self.depth or gameState.isWin() == True or gameState.isLose() == True):
                return self.evaluationFunction(gameState)                           #if pacman won or lost or we have reached the depth of our search return the evaluation function
            elif(agentIndex == 0):                                                  #if we are at pacman return the action with the max value
                return max_value(gameState, agentIndex, depth)
            elif(agentIndex != 0):                                                 #if we are at a ghost return the action with the min value
                return min_value(gameState, agentIndex, depth)

        bestAction = minimax(gameState, 0, 0)                                   #initialize minimax
        return bestAction[0]                                                    #return the best action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, agentIndex, depth, a ,b) :		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return self.evaluationFunction(gameState)               #if we are at a leaf return the evaluation function for that gamestate
            v = [None, float("-Inf")]
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)
                result = ABprun(currentState, agentIndex+1, depth, a, b)                     #simular logic with minimax
                if type(result)==list:
                    result = result[1]
                if v[1] < result:
                    v = [action,result]
                if v[1] > b:                            #if current v[1] is greater than b's value return that v  and don't search any farther
                    return v
                a = max(a, v[1])                            #make a the max between the current a and v[1]
            return v

        def min_value(gameState, agentIndex, depth, a, b) :		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return self.evaluationFunction(gameState)           #if we are at a leaf return the evaluation function for that gamestate
            v = [None, float("Inf")]
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)
                result = ABprun(currentState, agentIndex+1, depth, a, b)                     #simularlogic with minimax
                if type(result) == list:
                    result= result[1]
                if result < v[1]:
                    v = [action,result]
                if v[1] < a:                                                           #if current v[1] is less than a's value return that v  and don't search any farther
                    return v
                b = min(v[1], b)                                                                #make b the min between the current b and v[1]
            return v

        def ABprun(gameState, agentIndex, depth, a, b):

            if agentIndex == gameState.getNumAgents():      #if we searched all the agents for a certain depth go to the next and start anew
                depth = depth+1
                agentIndex = 0

            if( depth == self.depth or gameState.isWin() == True or gameState.isLose() == True):        #simular logic with minimax but for ABpruning
                return self.evaluationFunction(gameState)
            elif(agentIndex == 0):
                return max_value(gameState, agentIndex, depth, a, b)
            elif(agentIndex != 0):
                return min_value(gameState, agentIndex, depth, a, b)

        bestAction =ABprun(gameState, 0, 0, float("-Inf"), float("Inf"))
        return bestAction[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def max_value(gameState, agentIndex, depth):		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return self.evaluationFunction(gameState)           #if we are at a leaf return the evaluation function for that gamestate
            v = [None, float("-Inf")]
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)
                result = Expectimax(currentState, agentIndex+1, depth)                     #simular logic with minimax
                if type(result)==list:
                    result = result[1]
                if v[1] < result:
                    v = [action,result]
            return v

        def Chance(gameState, agentIndex, depth) :		#number of agents(gameState.getNumAgents) to perform max_value and current depth

            actions = gameState.getLegalActions(agentIndex)
            if len(actions) == 0:
                return self.evaluationFunction(gameState)               #if we are at a leaf return the evaluation function for that gamestate
            v = [None, 0.0]
            for action in actions:
                currentState = gameState.generateSuccessor(agentIndex, action)
                result = Expectimax(currentState, agentIndex+1, depth)
                if type(result) == list:
                    result= result[1]
                v[0] = action
                v[1] = v[1] + (result/len(actions))                         #the numerecial value for v[1] will be tha addition of itself with the average numerecial value its previous nodes
            return v

        def Expectimax(gameState, agentIndex, depth):

            if agentIndex == gameState.getNumAgents():      #if we searched all the agents for a certain depth go to the next and start anew
                depth = depth+1
                agentIndex = 0

            if( depth == self.depth or gameState.isWin() == True or gameState.isLose() == True):        #simular logic with minimax
                return self.evaluationFunction(gameState)
            elif(agentIndex == 0):
                return max_value(gameState, agentIndex, depth)
            elif(agentIndex != 0):
                return Chance(gameState, agentIndex, depth)

        bestAction = Expectimax(gameState, 0, 0)
        return bestAction[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()                                   #simular logic with evaluationFunction but for currentGameState and this time we are also looking at ghost states (for edible and non edible) ghosts
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    score =currentGameState.getScore()
    ghostBonus = 0.0
    for ghost in newGhostStates:                                                    #for all the ghosts in ghost States find the shortest distance from Pacman and if it leads to an edible ghost eat it or run away
        ghostDist = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if ghostDist > 0:
            if ghost.scaredTimer > 0:                                       #if qhost is edible go that way by giving a better score
                ghostBonus = ghostBonus + 50.0/ghostDist
            else:
                ghostBonus = ghostBonus - 30.0/ghostDist                      #if ghost is not edible run away by shortening the score
    score = score + ghostBonus

    foodDist = [manhattanDistance(newPos, x) for x in newFood.asList()]	               #find the closest distances to food
    if(len(foodDist)!=0):			                   #if there is still food in the list maximaze rhe score using shortest distance to food
		score = score+10.0/min(foodDist)			#same idea with ghost distance but this time it adds to the score, for 1 the scores where bad but 10 works better than any value i tried

    return score;
# Abbreviation
better = betterEvaluationFunction

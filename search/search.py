# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()                         #stack (fifo) where the items we search will be stored and then popped
    frontier.push(problem.getStartState())              #first element of the stack
    explored = []                                   #list of all the visited nodes
    parent = {}                                         #a dictionary where the state and action of each node's parent will bw held
    parent[problem.getStartState()] = (0, 0)        #the first node doesn't have a parent
    while(True):
        if(frontier.isEmpty() == True):         #if the frontier is empty we have found our goal state and we break our repetition inside while
            break
        else:
            current = frontier.pop()                #the first item of the stack is popped and we'll use that to search the graph
            if(problem.isGoalState(current) is True):
                path = []                               #if we have found our goal state we ceate a list that will contain of the states and the actions that got us there
                cur_prev = parent[current]
                path.append(cur_prev[1])
                while parent[cur_prev[0]] != (0, 0):
                    path.append(parent[cur_prev[0]][1])         #we keep putting the actions that lead us from parents to the nodes we are visiting in th path
                    cur_prev = parent[cur_prev[0]]

                solution = []
                for i in reversed(path):            #we reverse our path list because we've put the states from end to start
                    solution.append(i)
                return solution                 #we return the right ApproximateSearchAgent
            else:
                explored.append(current)                    #we add current state to the explore list so we won;t visit that agian
                for next_step in problem.getSuccessors(current):            #for all the successors of the current node if not in frontier and explore we add them
                    if((next_step[0] not in frontier.list) and (next_step[0] not in explored)):
                        frontier.push(next_step[0])
                        parent[next_step[0]] = (current, next_step[1])          #current is the parent node of the next_step, so we add that to the dictionairy along with the action that got us there
    return None

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()                 #same logic with bfs but with a queue(lifo)
    frontier.push(problem.getStartState())
    explored = []
    parent = {}
    parent[problem.getStartState()] = (0, 0)
    path = []
    if problem.isGoalState(problem.getStartState()) is True:
        return problem.getStartState()

    while(frontier.isEmpty() is False):
            current = frontier.pop()
            explored.append(current)
            for next_step in problem.getSuccessors(current):                                #in bfs on contrary with dfs we'll check every child node of current for goal State
                if((next_step[0] not in frontier.list) and (next_step[0] not in explored)):
                    parent[next_step[0]] = (current, next_step[1])
                    if(problem.isGoalState(next_step[0]) is True):
                        cur_prev = parent[next_step[0]]
                        path.append(cur_prev[1])
                        while parent[cur_prev[0]] != (0, 0):                    #doing a similar method as in dfs but for finding the right path
                            path.append(parent[cur_prev[0]][1])
                            cur_prev = parent[cur_prev[0]]
                        solution = []
                        for i in reversed(path):
                            solution.append(i)
                        return solution
                    else:
                        frontier.push(next_step[0])                 #if we haven't reachd the goal state add that node to the frontier

    return None
    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()                     #we use a priority queue to keep the cost of every edge
    frontier.push(problem.getStartState(),0)
    explored = []
    parent = {}
    parent[problem.getStartState()] = (0, 0, 0)         #the parent dictionary in thhat case will keep not only the state and the action but the cost of each path we take
    while(True):
        if(frontier.isEmpty() == True):
            break
        else:
            current = frontier.pop()
            if(problem.isGoalState(current) is True):           #same method as in dfs for finding the final path
                path = []
                cur_prev = parent[current]
                path.append(cur_prev[1])
                while parent[cur_prev[0]] != (0, 0, 0):
                    path.append(parent[cur_prev[0]][1])
                    cur_prev = parent[cur_prev[0]]

                solution = []
                for i in reversed(path):
                    solution.append(i)
                return solution
            else:
                explored.append(current)
                for next_step in problem.getSuccessors(current):
                    cost = next_step[2] + parent[current][2]                    #for every node we search the total cost equals the addition of each node before that plus the cost of the current node
                    if((next_step[0] not in [item[2]for item in frontier.heap]) and (next_step[0] not in explored)):
                        frontier.push(next_step[0], cost)
                        parent[next_step[0]] = (current, next_step[1], cost)

                    elif(next_step[0] in [item[2]for item in frontier.heap]) and (next_step[0] not in explored) and (cost<parent[next_step[0]][2]):       #if the node's already in frontier but the cost from the current path we are searching is smaller that the previous we followed to get there
                        frontier.update(next_step[0], cost)                                                                                                 #upgrade the frontier with the new cost and change the dictionary
                        parent[next_step[0]] = (current, next_step[1], cost)

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()                         #similar method with ucs but the path(he costs) will be found with a heuristic function
    frontier.push(problem.getStartState(),heuristic(problem.getStartState(),problem))
    explored = []
    parent = {}
    parent[problem.getStartState()] = (0, 0, 0)
    while(True):                                    #the usual technique as the rest
        if(frontier.isEmpty() == True):
            break
        else:
            current = frontier.pop()
            if(problem.isGoalState(current) is True):
                path = []
                cur_prev = parent[current]
                path.append(cur_prev[1])
                while parent[cur_prev[0]] != (0, 0, 0):
                    path.append(parent[cur_prev[0]][1])
                    cur_prev = parent[cur_prev[0]]

                solution = []
                for i in reversed(path):
                    solution.append(i)
                return solution

            else:
                explored.append(current)
                for next_step in problem.getSuccessors(current):
                    cost = next_step[2] + parent[current][2] + heuristic(next_step[0],problem)              #the cost this time will be equal with the cost of the path till the current node(next_step) plus the current node's cost plus the heuristic of the current node
                    if((next_step[0] not in [item[2]for item in frontier.heap]) and (next_step[0] not in explored)):
                        frontier.push(next_step[0],cost)
                        parent[next_step[0]] = (current, next_step[1], cost-heuristic(next_step[0],problem))
                    elif(next_step[0] in [item[2]for item in frontier.heap]) and (next_step[0] not in explored) and (cost<parent[next_step[0]][2]+heuristic(current, problem)):
                        frontier.update(next_step[0], cost)                                                 #if we found a better path to current node that the one that exists in frontier change the frontie to our new standars
                        parent[next_step[0]] = (current, next_step[1], cost-heuristic(next_step[0],problem))        #also change the current node's parent dictionary
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

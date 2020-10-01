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
import random, util, itertools

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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        print(legalMoves[chosenIndex])
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
        return successorGameState.getScore()

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions()
        move = legalMoves[0]
        max_value = -1000000
        for action in legalMoves:
            successorGameState = gameState.generateSuccessor(0, action)
            value = self.miniMaxFunction(successorGameState, self.depth, False)
            # print(f"value: {value}, action: {action}, score: {successorGameState.getScore()}, currentScore: {gameState.getScore()} ")
            if max_value <= value:
                max_value = value
                move = action
        # print(f'move: {move}')
        return move


    def miniMaxFunction(self, currentGameState, depth, is_pacman):
        # We want a tree where the successors to max is where pacman can move, and the
        # successors to min is where the ghosts can move. Min will always choose the position
        # in which the score is the lowest, and max will always choose the position
        # in which the score is the highest.

        # If depth is zero then we will evaluate the score of the current position:
        if depth == 0:
            return currentGameState.getScore()
        elif currentGameState.isLose():
            return currentGameState.getScore()
        elif currentGameState.isWin():
            return currentGameState.getScore()
        else:
            # If the depth is not zero then we will call the function again, with a boolean depending on the
            # input boolean
            if is_pacman:
                legalMoves = currentGameState.getLegalActions()
                max_val = -1000000
                for action in legalMoves:
                    successorGameState = currentGameState.generateSuccessor(0, action)
                    val = self.miniMaxFunction(successorGameState, depth, False)
                    max_val = max(max_val, val)
                return max_val

            else:
                depth -= 1
                agent_legal_move_list = []
                number_of_agents = currentGameState.getNumAgents()
                for i in range(1, number_of_agents):
                    agent_legal_move_list.append(currentGameState.getLegalActions(i))
                move_list = list(itertools.product(*agent_legal_move_list))
                min_val = 1000000

                for actions in move_list:
                    successorGameState = currentGameState
                    for i in range(1, number_of_agents):
                        if not successorGameState.isLose() and not successorGameState.isWin():
                            successorGameState = successorGameState.generateSuccessor(i, actions[i-1])
                    # At this point, successorGameState is up to date. All ghosts have made a move
                    if successorGameState.isLose():
                        val = successorGameState.getScore()
                    elif successorGameState.isWin():
                        val = successorGameState.getScore()
                    else:
                        val = self.miniMaxFunction(successorGameState, depth, True)
                    min_val = min(min_val, val)
                return min_val


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions()
        move = legalMoves[0]
        max_value = -1000000
        alpha = -1000000
        beta = 1000000

        for action in legalMoves:
            successorGameState = gameState.generateSuccessor(0, action)
            value = self.miniMaxFunction(successorGameState, self.depth, alpha, beta, False)
            if max_value <= value:
                max_value = value
                move = action
            alpha = max(value, alpha)
            if beta < alpha:
                break
        return move

    def miniMaxFunction(self, currentGameState, depth, alpha, beta, is_pacman):
        # We want a tree where the successors to max is where pacman can move, and the
        # successors to min is where the ghosts can move. Min will always choose the position
        # in which the score is the lowest, and max will always choose the position
        # in which the score is the highest.

        # If depth is zero then we will evaluate the score of the current position:
        if depth == 0:
            return currentGameState.getScore()
        elif currentGameState.isLose():
            return currentGameState.getScore()
        elif currentGameState.isWin():
            return currentGameState.getScore()
        else:
            # If the depth is not zero then we will call the function again, with a boolean depending on the
            # input boolean
            if is_pacman:
                legalMoves = currentGameState.getLegalActions()
                max_val = -1000000
                for action in legalMoves:
                    successorGameState = currentGameState.generateSuccessor(0, action)
                    val = self.miniMaxFunction(successorGameState, depth, alpha, beta, False)
                    max_val = max(max_val, val)
                    alpha = max(alpha, val)
                    if beta < alpha:
                        break
                return max_val

            else:
                depth -= 1
                agent_legal_move_list = []
                number_of_agents = currentGameState.getNumAgents()
                for i in range(1, number_of_agents):
                    agent_legal_move_list.append(currentGameState.getLegalActions(i))
                move_list = list(itertools.product(*agent_legal_move_list))
                min_val = 1000000

                for actions in move_list:
                    successorGameState = currentGameState
                    for i in range(1, number_of_agents):
                        if not successorGameState.isLose() and not successorGameState.isWin():
                            successorGameState = successorGameState.generateSuccessor(i, actions[i - 1])
                    # At this point, successorGameState is up to date. All ghosts have made a move
                    if successorGameState.isLose():
                        val = successorGameState.getScore()
                    elif successorGameState.isWin():
                        val = successorGameState.getScore()
                    else:
                        val = self.miniMaxFunction(successorGameState, depth, alpha, beta, True)
                    min_val = min(min_val, val)
                    beta = min(beta, val)
                    if beta < alpha:
                        break
                return min_val

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

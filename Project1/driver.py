import sys
from search import *

class State:
    """
    Should be an abstract class valid for a given problem. For simplicity, now 
    only works with the 8-puzzle problem. This class defines a State for the N
    puzzle problem.
    """
    def __init__(self, board, zero, cost, prev = None, action = None):
        self.board = [list(b) for b in board]
        self.cost = cost
        self.zero = zero
        self.prev = prev
        self.action = action

    def isGoal(self):
        for i in range(3):
            for j in range(3):
                if (3*i + j) != self.board[i][j]:
                    return False
        return True
    def getActions(self):
        """
        Returns a list of available actions from the current state.
        """
        actions = []
        i = self.zero[0]
        j = self.zero[1]
        if i > 0:
            actions.append('Up')
        if i < 2:
            actions.append('Down')
        if j > 0:
            actions.append('Left')
        if j < 2:
            actions.append('Right')
        return actions

    def expand(self):
        """
        Returns a list of states, that are the result of applying
        a list of actions to a current state (successor states)
        """
        actions = self.getActions()
        successors = []
        i, j = self.zero
        for action in actions:
            board = [list(b) for b in self.board]
            if action == 'Up':
                board[i][j] = self.board[i-1][j]
                board[i-1][j] = 0
                successors.append(State(board, (i-1, j), self.cost + 1, self, action))
            elif action == 'Down':
                board[i][j] = self.board[i+1][j]
                board[i+1][j] = 0
                successors.append(State(board, (i+1, j), self.cost + 1, self, action))
            elif action == 'Left':
                board[i][j] = self.board[i][j - 1]
                board[i][j - 1] = 0
                successors.append(State(board, (i, j-1), self.cost + 1, self, action))
            elif action == 'Right':
                board[i][j] = self.board[i][j + 1]
                board[i][j+1] = 0
                successors.append(State(board, (i, j+1), self.cost + 1, self, action))
        return successors


    def __eq__(self, other):
        """
        """
        for row in range( 3 ):
            if self.board[row] != other.board[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        s = "Current moves: " + str(self.cost) + "\n"
        s += "Zero Position: " + str(self.zero) + "\n"
        s += "Board:\n"
        s += '\n'.join([' '.join(str(y) for y in w) for w in self.board ])
        return s

class Npuzzle(Problem):
    """
    This class is an implementation of the Npuzzle as a search problem. It contains
    the definitions for the methods needed to apply search algorithms.
    """
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        return state.expand()
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python driver.py <method> <board>'
        sys.exit(0)

    # Processing command line arguments
    method = sys.argv[1]
    board = [int(i) for i in sys.argv[2].split(",")]
    board = [board[i:i+3] for i in range(0, len(board), 3)]
    zero = next(((i, array.index(0))
        for i, array in enumerate(board)
        if 0 in array),
        None)
    
    state = State(board, zero, 0)
    problem = Npuzzle(state)
    solver = Solver()

    # TODO: Add cases that uses A-start and the rest of algorithms that are going to be implemented
    if method == 'bfs':
        solver.breadthFirstSearch(problem)
    else:
        solver.depthFirstSearch(problem)

    # Writing to output file
    with open("output.txt", "w") as text_file:
        text_file.write("path_to_goal: ") 
        text_file.write(str(solver.path) + "\n")
        text_file.write("cost_of_path: ") 
        text_file.write(str(solver.cost_of_path) + "\n")
        text_file.write("nodes_expanded: ")
        text_file.write(str(solver.nodes_expanded) + "\n")
        text_file.write("fringe_size: ")
        text_file.write(str(solver.fringe_size) + "\n")
        text_file.write("max_fringe_size: ")
        text_file.write(str(solver.max_fringe_size) + "\n")
        text_file.write("search_depth: ")
        text_file.write(str(solver.search_depth) + "\n")
        text_file.write("max_search_depth: ")
        text_file.write(str(solver.max_search_depth) + "\n")
        text_file.write("running_time: ")
        text_file.write(("%.8f") % solver.running_time + "\n")
        text_file.write("max_ram_usage: ")
        text_file.write(("%.8f") % solver.max_ram_usage + "\n")

# Sudoku_solver - created by Matt Herrero on 1/4/17
# See github "README.md" for description of program and how to use

import pdb
import os
from copy import deepcopy

def print_board(board):
  line = "________________________________"
  for i in range(len(board)):
    row = board[i]
    if (i)%3 == 0: print line
    print_str = ""
    for j in range(len(row)):
      if j%3 == 0: print_str += "|"
      if board[i][j] < 0:
        print_str += "_ "
      else:
        print_str += str(board[i][j]) + " "
    print print_str

grid_ind_map = {(0,0): 0, (1,0): 0, (2,0): 0, (0,1): 0, (1,1): 0, (2,1): 0, (0,2): 0, (1,2): 0, (2,2): 0,
                (3,0): 1, (4,0): 1, (5,0): 1, (3,1): 1, (4,1): 1, (5,1): 1, (3,2): 1, (4,2): 1, (5,2): 1,
                (6,0): 2, (7,0): 2, (8,0): 2, (6,1): 2, (7,1): 2, (8,1): 2, (6,2): 2, (7,2): 2, (8,2): 2,
                (0,3): 3, (1,3): 3, (2,3): 3, (0,4): 3, (1,4): 3, (2,4): 3, (0,5): 3, (1,5): 3, (2,5): 3,
                (3,3): 4, (4,3): 4, (5,3): 4, (3,4): 4, (4,4): 4, (5,4): 4, (3,5): 4, (4,5): 4, (5,5): 4,
                (6,3): 5, (7,3): 5, (8,3): 5, (6,4): 5, (7,4): 5, (8,4): 5, (6,5): 5, (7,5): 5, (8,5): 5,
                (0,6): 6, (1,6): 6, (2,6): 6, (0,7): 6, (1,7): 6, (2,7): 6, (0,8): 6, (1,8): 6, (2,8): 6,
                (3,6): 7, (4,6): 7, (5,6): 7, (3,7): 7, (4,7): 7, (5,7): 7, (3,8): 7, (4,8): 7, (5,8): 7,
                (6,6): 8, (7,6): 8, (8,6): 8, (6,7): 8, (7,7): 8, (8,7): 8, (6,8): 8, (7,8): 8, (8,8): 8}

def get_nums_in_row(board, row_ind):
  assert(row_ind < 9 and row_ind > -1)
  row = board[row_ind]
  return list(set([x for x in row if x > -1]))

def get_nums_in_col(board, col_ind):
  assert(col_ind < 9 and col_ind > -1)
  col = []
  for row in board:
    col.append(row[col_ind])
  return list(set([x for x in col if x > 0]))

def get_nums_in_grid(board, row_ind, col_ind):
  assert(row_ind < 9 and row_ind > -1)
  assert(col_ind < 9 and col_ind > -1)

  grid_ind = grid_ind_map.get((col_ind, row_ind))

  def get_col_inds():
    if grid_ind in [0, 3, 6]:
      return [0, 1, 2]
    elif grid_ind in [1, 4, 7]:
      return [3, 4, 5]
    else:
      return [6, 7, 8]

  def get_row_inds():
    if grid_ind < 3:
      return [0, 1, 2]
    elif grid_ind > 5:
      return [6, 7, 8]
    else:
      return [3, 4, 5]

  grid_nums = []
  col_inds = get_col_inds()
  row_inds = get_row_inds()
  for row_ind in row_inds:
    for col_ind in col_inds:
      if board[row_ind][col_ind] not in grid_nums:
        grid_nums.append(board[row_ind][col_ind])
  return grid_nums

def is_legal(board, row_ind, col_ind, poss_fill):
  row_nums = get_nums_in_row(board, row_ind)
  col_nums = get_nums_in_col(board, col_ind)
  grid_nums = get_nums_in_grid(board, row_ind, col_ind)
  return (poss_fill not in row_nums) and (poss_fill not in col_nums) and (poss_fill not in grid_nums)

class SudokuGame:
  def __init__(self, given_nums, rows, cols):
    self.given_nums = given_nums
    self.rows = rows
    self.cols = cols

  #state = board, next_position tuple
  def start_state(self):
    board = [[-1 for x in range(self.cols)] for y in range(self.rows)]
    for coord in self.given_nums:
      board[coord[1]][coord[0]] = self.given_nums.get(coord)
    return (board, (0,0))

  def is_end(self, state):
    if (state[1] == (0, self.rows)):
      return 1
    else:
      return 0

  def actions(self, state):
    return [x for x in xrange(1, 10)]

  def succ(self, state, action):
    #change the board
    cur_board = deepcopy(state[0])
    next_col, next_row = state[1]
    cur_board[next_row][next_col] = action
    #change the next_position tuple
    if(next_col >= 8):
      next_col = 0
      next_row += 1
    else:
      next_col += 1
    return (cur_board, (next_col, next_row))

def solve_board(sudoku_game):

  def recursion_step(sudoku_game, state):
    curr_board = state[0]
    next_col = state[1][0]
    next_row = state[1][1]

    if sudoku_game.is_end(state):
      return curr_board

    if state[0][next_row][next_col] > 0:
      return recursion_step(sudoku_game, sudoku_game.succ(state, state[0][next_row][next_col]))

    for action in sudoku_game.actions(state):
      if is_legal(curr_board, next_row, next_col, action):
        board_result = recursion_step(sudoku_game, sudoku_game.succ(state, action))
        if board_result: return board_result
    return None

  start_state = sudoku_game.start_state()
  print_board(start_state[0])
  raw_input("\nConfirm board (hit enter to continue): ")
  print("Solving the board... hold tight...")
  return recursion_step(sudoku_game, sudoku_game.start_state())
  

#given = {(4,0): 6, (5,0): 4, (6,0): 9, (8,0): 8,
#         (0,1): 5, (5,1): 9, (8,1): 7,
#         (6,2): 3, (7,2): 4,
#         (2,3): 9, (4,3): 1, (8,3): 6,
#         (0,4): 7, (1,4): 8, (7,4): 9, (8,4): 5,
#         (0,5): 6, (4,5): 5, (6,5): 2,
#         (1,6): 2, (2,6): 5,
#         (0,7): 8, (3,7): 2, (8,7): 1,
#         (0,8): 4, (2,8): 7, (3,8): 6, (4,8): 8}

# Describes the initial state of the board, maps grid coordinates
# to starting values, if starting value is specified
given = {(0,0): 1, (8,0): 7,
         (3,1): 7, (5,1): 8, (8,1): 1,
         (1,2): 3, (4,2): 4, (5,2): 5, (7,2): 9, (8,2): 2,
         (1,3): 7, (3,3): 8,
         (2,4): 8, (6,4): 5,
         (5,5): 9, (7,5): 1,
         (0,6): 7, (1,6): 4, (3,6): 5, (4,6): 3, (7,6): 2,
         (0,7): 9, (3,7): 2, (5,7): 6,
         (0,8): 2, (8,8): 3}


game = SudokuGame(given, 9, 9)
solved_board = solve_board(game)
print "\nSolved! \n"


while(1):
  sol_or_slot = ""
  while(1):
    sol_or_slot = raw_input("Do you want to print the solution, or reveal a single slot?\n(input \"solution\" for the whole solution, \"slot\" for a single slot, or \"quit\" to quit): ")
    if (sol_or_slot != "solution" and sol_or_slot != "slot" and sol_or_slot != "quit"):
      print "\nI dunno what you meant by \"" + sol_or_slot + ",\" let's try that again...\n"
    else:
      break
  if sol_or_slot == "solution":
    print "\nFull solution is..."
    print_board(solved_board)
    break
  elif sol_or_slot == "slot":
    while(1):
      reveal_col = int(raw_input("\nInput the column of the box you want to reveal: "))
      reveal_row = int(raw_input("Input the row of the box you want to reveal: "))
      if not ((reveal_row in range(9)) and (reveal_col in range(9))):
        print "\nI can't find a grid at (" + str(reveal_col) + "," + str(reveal_row) + "), let's try again..."
      else:
        break
    print "\n" + str(solved_board[reveal_row][reveal_col]) + "\n"
  elif sol_or_slot == "quit":
    break




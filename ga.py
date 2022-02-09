import sys
import numpy
import random 

#Puzzle 1 - Number Allocation
def p1_number_allocation():
    return 0

#Puzzle 2 - Tower Building
def p2_tower_building():
    return 0

if __name__ == '__main__':
    # command line inputs
    program_name = sys.argv[0]
    # puzzle to solve
    puzzle_id = int(sys.argv[1])
    # input file
    file_name = sys.argv[2]
    # time to solve
    problem_time = int(sys.argv[3])

    if(puzzle_id == 1):
        #Run Number Allocation Puzzle
        p1_number_allocation()
    elif(puzzle_id == 2):
        #Run Tower Builder Puzzle
        p2_tower_building()
    else:
        print("Incorrect Puzzle Identifier")
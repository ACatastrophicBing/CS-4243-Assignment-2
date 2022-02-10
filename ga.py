import string
import sys
import numpy
import random
import time
import array
from pathlib import Path

#Puzzle 1 - Number Allocation
def p1_number_allocation():
    return 0

#Todo - TB Helper Functions
class Tower_piece:
    def __init__(self, type:string, width:int, strength:int, cost:int):
        self.type = type
        self.width = width
        self.strength = strength
        self.cost = cost
    
    def toString(self):
        print(f"{self.type}, {self.width}, {self.strength}, {self.cost}")
    


def tower_fitness(score:int):
    return 0

#Returns an array of Tower_pieces
def pieces2arr(file):
    piece_list = []

    with open(file, "r") as f:
        for line in f:
            stripped_line = line.rstrip()
            temp_piece = stripped_line.split(", ")
            temp_Tower_piece = Tower_piece(temp_piece[0], temp_piece[1], temp_piece[2], temp_piece[3])
            piece_list.append(temp_Tower_piece)

    return piece_list

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

    #Incorrect file handler
    file_path = Path(file_name)
    if(file_path.is_file() != True):
        print(f"Incorrect file path. {file_path} does not exist")
        exit()

    # time to solve
    problem_time = int(sys.argv[3])

    if(puzzle_id == 1):
        #Run Number Allocation Puzzle
        start_time = time.time()
        while (time.time() - start_time) < problem_time:
            p1_number_allocation()
            
    elif(puzzle_id == 2):
        #Run Tower Builder Puzzle
        start_time = time.time()
        while (time.time() - start_time) < problem_time:
            p2_tower_building()

    else:
        print("Incorrect Puzzle Identifier")
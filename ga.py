import string
import sys
import numpy
import random
import time
import array
from pathlib import Path


def bucket_distributor(numList):
    bucket1 = {}
    bucket2 = {}
    bucket3 = {}
    bucket4 = {}
    for i in range(9):
        bucket1.update({i : numList[i]})
    for i in range(10, 19):
        bucket2.update({i : numList[i]})
    for i in range(20, 29):
        bucket3.update({i : numList[i]})
    for i in range(30, 39):
        bucket4.update({i : numList[i]})
    return bucket1, bucket2, bucket3, bucket4

#Puzzle 1 Solve
def p1_genetic_solver(population):
    """
    :param population: Takes in a list of 4 bins
    :return: new population
    """
    culling_factor = 30 # What percentage of population we are culling
    fitness = p1_fitness(population)

    return population

# Can edit this to take in certain factors like wanted population size to handle the next population selection instead
def p1_fitness(population):
    """
    :param population: Takes in a population(list of 4 bins) and finds the fitness for each parent
    :return fitness: A list of cumulative percentages for each parent to be chosen
    """
    k = 1 # fitness multiplier
    fitness = []
    for parent in population:
        fitness.append(bin1_score(parent[0]) + bin2_score(parent[1]) + bin3_score(parent[2])) # Subtract bin4_score if we want to use it
    fitness_sum = sum(fitness)
    return fitness/fitness_sum

def bin1_score(bin):
    score = 1
    for gene in bin:
        score *= gene
    return score

def bin2_score(bin):
    score = 0
    for gene in bin:
        score += gene
    return score

def bin3_score(bin):
    score = max(bin) - min(bin)

def bin4_score(bin):
    score = 0
    for gene in bin:
        score += abs(gene)
    return score

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

    file_data = [0]*40 # TODO : Need to set this equal to file data

    # time to solve
    problem_time = int(sys.argv[3])

    if(puzzle_id == 1):
        #Run Number Allocation Puzzle
        start_time = time.time()
        population = bucket_distributor(file_data)
        while (time.time() - start_time) < problem_time:
            population = p1_genetic_solver(population)


    elif(puzzle_id == 2):
        #Run Tower Builder Puzzle
        start_time = time.time()
        while (time.time() - start_time) < problem_time:
            p2_tower_building()

    else:
        print("Incorrect Puzzle Identifier")
import string
import sys
import numpy
import random
import time
import array
from pathlib import Path


def mutate(x):
    """
    :param x: percentage of chance to mutate (0 to 100)
    :return boolean: If it is within the x% chance we set for mutation, mutate
    """
    return random.uniform(0, 1) <= x/100

def bucket_distributor(numList):
    bucket1 = [0]*10
    bucket2 = [0]*10
    bucket3 = [0]*10
    bucket4 = [0]*10
    parent = []
    for i in range(10):
        bucket1[i] = numList[i]
    parent.append(bucket1)
    for i in range(10, 20):
        bucket2[i-10] = numList[i]
    parent.append(bucket2)
    for i in range(20, 30):
        bucket3[i-20] = numList[i]
    parent.append(bucket3)
    for i in range(30, 40):
        bucket4[i-30] = numList[i]
    parent.append(bucket4)
    return [bucket1, bucket2, bucket3, bucket4]

def population_maker(parent):
    population = []
    for i in range(10): #Changed to 10 for easier debugging
        population.append(crossover(parent))
    return population

def crossover(parent):
    swap_1, swap_2 = random.sample(range(4), 2)
    selection = random.sample(range(10),4)
    selection = [x + 1 for x in selection]
    swap_1_indeces = random.sample(range(10), len(selection))
    swap_2_indeces = random.sample(range(10), len(selection))
    # TODO For some reason the allocations in memory are crossing over, needs a fix
    # TODO Also, for some reason there seems to be a point in which the indexing doesn't work, causing duplicates which is bad
    print(swap_1)
    print(parent[swap_1])
    chromosome1 = parent[swap_1]
    chromosome2 = parent[swap_2]
    placeholder_chromosome2 = parent[swap_2]
    # print("Swapping bin %d and have the stuff %s" %(swap_1+1,parent[swap_1]))
    for i in range(len(selection)):
        chromosome2[swap_2_indeces[i]] = chromosome1[swap_1_indeces[i]]
        chromosome1[swap_1_indeces[i]] = placeholder_chromosome2[swap_2_indeces[i]]
    parent[swap_1] = chromosome1
    parent[swap_2] = chromosome2
    return parent

#Puzzle 1 Solve
def p1_genetic_solver(parent):
    """
    :param population: Takes in a list of 4 bins
    :return: new population
    """
    culling_factor = 30 # What percentage of population we are culling
    mutation_factor = 5
    population = population_maker(parent)
    if mutate(mutation_factor):
        parent_mutating = random.sample(range(len(population)),1)
        population[parent_mutating[0]] = crossover(population[parent_mutating[0]])
    fitness = p1_fitness(population)
    max_fitness = max(fitness)
    best_parent = fitness.index(max_fitness)
    print("Finished")
    return population[best_parent]

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
    fit_weight = []
    prev_fit = 0
    for i in range(len(fitness)):
        fit_weight.append(fitness[i]/fitness_sum + prev_fit)
        prev_fit += fitness[i] / fitness_sum
    return fit_weight

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
    return score

def bin4_score(bin):
    score = 0
    for gene in bin:
        score += abs(gene)
    return score

#Todo - TB Helper Functions
class Tower_piece:
    """
    Tower_piece object | type of piece, width, strength and cost
    toString | returns the tower_piece in an easy to read format
    """
    def __init__(self, type:string, width:int, strength:int, cost:int):
        self.type = type
        self.width = width
        self.strength = strength
        self.cost = cost
    
    def toString(self):
        return(f"{self.type}, {self.width}, {self.strength}, {self.cost}")

class Tower:
    '''
    __init__ pass in array of pieces, can be empty
    print_pieces | print all pieces within the tower
    getScore | returns score
    add_piece | appends a piece to the tower
    tower_fitness | calculates score + fitness of the tower withn all 5 restrictions
    '''
    def __init__(self, pieces:array):
        #0 is false, 1 is true, -1 is not set 
        self.valid = -1
        self.score = -1
        self.pieces = pieces

    def print_pieces(self):
        for piece in self.pieces:
            print(piece.toString())

    def getScore(self):
        return self.score

    #Adds a piece to the Tower array. 
    def add_piece(self, piece:Tower_piece):
        self.pieces.append(piece)

    def tower_fitness(self):
        #Check if base is a Door
        if(self.pieces[0].type != "Door"):
            self.score = 0
            self.valid = 0
            return
        #Check if top is a Lookout
        if(self.pieces[len(self.pieces)-1].type != "Lookout"):
            self.score = 0
            self.valid = 0
            return
        
        #Check if the base can support the pieces placed on top
        root_piece_strength = self.pieces[0].strength
        if(root_piece_strength < len(self.pieces) - 1):
            self.score = 0
            self.valid = 0
            return

        #Check if middle pieces are walls and width restrictions
        for index in range(1, len(self.pieces) - 1):
            #Grabs the prior piece in the list
            prev_piece = self.pieces[index-1]

            current_piece = self.pieces[index]

            #Check if middle pieces are walls and if the width restrictions are voided
            if(current_piece.type != "Wall" or prev_piece.width < current_piece.width):
                self.score = 0
                self.valid = 0
                return
            else:
                continue
        
        #Calculate cost of the tower assuming all prior tests have passed
        cumulative_cost = -1 
        for piece in self.pieces:
            cumulative_cost += piece.cost

        self.score = (10+(len(self.pieces) ** 2) - (cumulative_cost))

#Returns an array of Tower_pieces
def pieces2arr(file):
    piece_list = []

    #Reads file and strips newline and separates by comma
    with open(file, "r") as f:
        for line in f:
            stripped_line = line.rstrip()
            temp_piece = stripped_line.split(", ")
            temp_Tower_piece = Tower_piece(temp_piece[0], int(temp_piece[1]), int(temp_piece[2]), int(temp_piece[3]))
            piece_list.append(temp_Tower_piece)

    #A list of ALL pieces passed in by the file
    return piece_list

#Returns an array of numbers
def numbers2arr(file):
    numbers = []

    with open(file,"r") as f:
        for line in f:
            stripped_line = line.rstrip()
            numbers.append(float(stripped_line))

    return numbers

#Puzzle 2 - Tower Building
def p2_tower_building():
    return 0

'''
def tower_testing(file):
    piece_list = pieces2arr(file)
    t_pieces = [piece_list[0], piece_list[1], piece_list[5]]
    t2_pieces = [piece_list[0], piece_list[3]]

    Tower1 = Tower(t_pieces)
    Tower2 = Tower(t2_pieces)

    Tower1.tower_fitness()
    Tower2.tower_fitness()
    
    Tower1.print_pieces()
    Tower2.print_pieces()

    print(Tower1.getScore())

    print(Tower2.getScore())

    return 0

'''

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
        #TODO: Never seems to end
        start_time = time.time()
        file_data = numbers2arr(file_name)
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
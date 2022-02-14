import statistics
import string
import sys
import numpy
import random
import time
import array
from pathlib import Path

best_part1 = None
bestscore_part1 = 0

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
    for i in range(400): #This is our population size, basically we make a population of 100 every generation
        population.append(crossover(parent))
    return population

def crossover(parent):
    swap_1, swap_2 = random.sample(range(4), 2)
    selection = random.sample(range(10),4)
    selection = [x + 1 for x in selection]
    swap_1_indeces = random.sample(range(10), len(selection))
    swap_2_indeces = random.sample(range(10), len(selection))
    # print(swap_1)
    # print(parent[swap_1])
    chromosome1 = parent[swap_1].copy()
    chromosome2 = parent[swap_2].copy()
    placeholder_chromosome2 = parent[swap_2].copy()
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


    ### READ HERE :
    # These next three lines are if you just want to select the best fit of each population
    # The next_parent return below is for randomized selection based off of the fitness
    # max_fitness = max(fitness)
    # best_parent = fitness.index(max_fitness)
    # return population[best_parent]

    next_parent = population[childSelector(fitness)]
    return next_parent
    # print("Parent Found")

# Can edit this to take in certain factors like wanted population size to handle the next population selection instead
def p1_fitness(population):
    """
    :param population: Takes in a population(list of 4 bins) and finds the fitness for each parent
    :return fitness: A list of cumulative percentages for each parent to be chosen
    """
    k = 2 # fitness exponential
    global best_part1
    global bestscore_part1
    global worst_part1
    global worstscore_part1
    global mid_part1
    global midscore_part1
    fitness = []
    for parent in population:
        fitness.append(((bin1_score(parent[0]) + bin2_score(parent[1]) + bin3_score(parent[2]) - bin4_score(parent[3]) ** 3)) ** k) # Subtract bin4_score if we want to use it
        # putting this to the power of K to allow for bigger scores to be weighted differently if you want their value to be higher
        # Change k for different results
        # Also the abs value is since what if there's like a cool MASSIVE negative number?
        if scoring(parent) > bestscore_part1: # This is what finds the best fit
            best_part1 = parent.copy()
            bestscore_part1 = scoring(best_part1)
            print('best: ')
            print(bestscore_part1)
        if scoring(parent) < worstscore_part1: # This is what finds the worst fit
            worst_part1 = parent.copy()
            worstscore_part1 = scoring(worst_part1)
            print('worst: ')
            print(worstscore_part1)
    fitness_sum = sum(fitness)
    fit_weight = []
    prev_fit = 0
    for i in range(len(fitness)):
        fit_weight.append(fitness[i]/fitness_sum + prev_fit)
        prev_fit += fitness[i] / fitness_sum
    fitness.copy().sort()
    midscore_part1 = ((fitness[4] + fitness[5]) / 2)
    return fit_weight

def childSelector(fitness):
    """
    :param fitness: takes in the fitness list and randomly generates a number in between 0 and 1 to figure out what child the algorithm is keeping
    :return prev_index: The index for the child that is being kept
    """
    selection = random.uniform(0, 1)
    prev_index = -1
    for fit in fitness:
        if abs(fit) >= selection: # Using absolute value since there might be an instance in which we want a high boi
            break
        else:
            prev_index += 1
    return prev_index

def scoring(parent):
    return bin1_score(parent[0]) + bin2_score(parent[1]) + bin3_score(parent[2])

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
    program_name = '__main__'
    # puzzle to solve
    puzzle_id = 1
    # input file
    file_name = 'p1_testing.txt'

    #Incorrect file handler
    file_path = Path(file_name)
    if(file_path.is_file() != True):
        print(f"Incorrect file path. {file_path} does not exist")
        exit()

    # time to solve
    problem_time = 30
    if(puzzle_id == 1):
        #Run Number Allocation Puzzle
        #TODO: Never seems to end
        start_time = time.time()
        file_data = numbers2arr(file_name)
        population = bucket_distributor(file_data)
        best_part1 = population.copy()
        bestscore_part1 = scoring(best_part1)

        median_part1 = population.copy()
        medianscore_part1 = scoring(median_part1)

        worst_part1 = population.copy()
        worstscore_part1 = scoring(worst_part1)
        print("Starting")
        while (time.time() - start_time) < problem_time:
            population = p1_genetic_solver(population)
        print("Best list is :")
        print(best_part1)
        print("With a score of %f " % bestscore_part1)
        print("Median list is :")
        print(midscore_part1)
        print("With a score of %f " % medianscore_part1)
        print("Worst list is :")
        print(worst_part1)
        print("With a score of %f " % worstscore_part1)


    elif(puzzle_id == 2):
        #Run Tower Builder Puzzle
        start_time = time.time()
        while (time.time() - start_time) < problem_time:
            p2_tower_building()

    else:
        print("Incorrect Puzzle Identifier")
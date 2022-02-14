import string
import sys
import numpy as np
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
    max_fitness = max(fitness)
    best_parent = fitness.index(max_fitness)
    # print("Parent Found")
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
    eq | allows for comparison between pieces
    """
    def __init__(self, type:string, width:int, strength:int, cost:int):
        self.type = type
        self.width = width
        self.strength = strength
        self.cost = cost
    
    def toString(self):
        return(f"{self.type}, {self.width}, {self.strength}, {self.cost}")

    def __eq__(self, other): 
        if not isinstance(other, Tower_piece):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.type == other.type and self.width == other.width and self.strength == other.strength and self.cost == other.cost

class Tower:
    '''
    __init__ pass in array of pieces, can be empty
    print_pieces | print all pieces within the tower
    getScore | returns score
    add_piece | appends a piece to the tower
    tower_fitness | calculates score + fitness of the tower withn all 5 restrictions
    getPieces | returns list of pieces
    setPieces | set piece list of a tower

    '''
    def __init__(self, pieces:array):
        #0 is false, 1 is true, -1 is not set 
        self.valid = -1
        self.score = -1
        self.pieces = pieces

    def print_pieces(self):
        for piece in self.pieces:
            print(piece.toString())
    
    def setPieces(self, arr):
        self.pieces = arr
    
    def getPieces(self):
        return self.pieces

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

'''
Create an array of tower_pieces
Pass in the file containing the pieces

Return an array of all pieces
'''
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

'''
Create randomized population of n towers
Pass in an array of pieces and the number of towers to be generated

Returns entire population
'''

def create_tower_population(total_piece_arr, n:int):
    population_return = []
    #For each tower in the population
    for i in range(n):
        num_to_select = random.randint(1, len(total_piece_arr))
        #Select num_to_select random pieces from the piece array
        pieces_to_use = random.sample(total_piece_arr, num_to_select)
        random.shuffle(pieces_to_use)
        temp_tower = Tower(pieces_to_use)
        temp_tower.tower_fitness()

        population_return.append(temp_tower)
    
    return population_return

'''
Removes bottom 30% of towers from the population
Pass in an [Tower]
Returns a culled population
'''
def tower_culling(arr):
    #from 0-1
    cull_amount_percent = .30
    amt_to_cull = round(len(arr) * cull_amount_percent)

    #Sorts by highest score. i.e max score index 0, lowest at n-1 index
    arr.sort(key=lambda x: x.score, reverse=True)
    new_arr = []
    for n in range((len(arr) - amt_to_cull)):
        new_arr.append(arr[n])

    return new_arr

'''
Performs crossover over entire population
Pass in the population array [Tower]

Returns the new population with crossovers
'''
def tower_crossover(arr):
    new_tower_arr = []
    #No crossover if there is less than 3 in the population. Want to keep max score parent in tact
    if(len(arr) < 3):
        return arr
    
    #Do crossover of pieces
    iterable = 2
    while iterable < len(arr) - 1:
        tower_one = arr[iterable] #1st to swap
        tower_two = arr[iterable + 1] #2nd to swap
        print(tower_one.printPieces())

        pieces_to_swap_amt = len(tower_one.getPieces())//2
        pieces_to_swap_t2 = len(tower_two.getPieces())//2
        t1_swappable = tower_one.getPieces()[:pieces_to_swap_amt]
        t2_swappable = tower_two.getPieces()[:pieces_to_swap_t2]

        new_t1 = Tower(t1_swappable + tower_one.getPieces()[len(tower_one.getPieces()) - pieces_to_swap_amt:])
        new_t2 = Tower(t2_swappable + tower_two.getPieces()[len(tower_two.getPieces()) - pieces_to_swap_t2:])

        new_t1.tower_fitness()
        new_t2.tower_fitness()
        
        new_tower_arr.append(new_t1)
        new_tower_arr.append(new_t2)
        iterable += 2

    return new_tower_arr

'''
Check for duplicates in a list of pieces
Pass in an array of pieces to check for duplicates

Returns a list of indices of duplicate pieces in a tower
'''
def check_duplicate_pieces(piece_array):
    duplicate_tracker = []
    index_array = []

    count = 0
    for piece in piece_array:
        if piece in duplicate_tracker:
            index_array.append(count)
            count+=1
        else:
            duplicate_tracker.append(piece)
            count+=1
    return index_array
            
'''
Mutates and removes existing towers
Take array of all towers AND the global piece list from the file

Returns [Tower] i.e the whole population 
'''
def tower_mutation(tower_arr, global_pieces):
    new_tower_arr = []
    random_num = random.uniform(0,1)
    random_chance = 0.7

    for tower in tower_arr:
        duplicate_indices = check_duplicate_pieces(tower.getPieces())
        if duplicate_indices:
            for index in duplicate_indices:
                tower.getPieces().pop[index]
                tower.setPieces(tower.getPieces())
            tower.tower_fitness()
            new_tower_arr.append(tower)
        else:
            flag = True
            while flag:
                if(random_num > random_chance):
                    print("hello")
                    piece = random.choice(global_pieces)
                    print(piece.toString())
                    tower_pieces = tower.getPieces()
                    tower_pieces.append(piece)
                    if check_duplicate_pieces(tower_pieces) == False:
                        print("hello2")
                        tower.setPieces(tower_pieces)
                        flag = False
                        break
                    else:
                        continue
                flag = False
            tower.tower_fitness()
            new_tower_arr.append(tower)

        #random mutation
    #for tower in tower_arr:
        
    return new_tower_arr

'''
Repopulates with new towers to fill to original population size.
pieces_arr is array of all pieces
current_towers is existing tower population
population_size is original population

returns a [Tower] with originals + new population
'''
def tower_repopulation(pieces_arr, current_towers, population_size):
    current_pop = len(current_towers)
    new_pop = create_tower_population(pieces_arr, population_size-current_pop)
    
    full_pop = current_towers + new_pop

    return full_pop

#Puzzle 2 - Tower Building
def p2_tower_building(file):
    #Place file pieces into array for fetching
    all_pieces_arr = pieces2arr(file)
    '''
    POPULATION NUMBER | TO BE SET
    '''
    population_num = 3
    population = create_tower_population(all_pieces_arr, population_num)

    print("Gen 0")
    for p in population:
        print("Tower")
        p.print_pieces()
        print("\n")
    

    population = tower_culling(population)
    population = tower_crossover(population)
    population = tower_mutation(population, all_pieces_arr)
    population = tower_repopulation(all_pieces_arr, population, population_num)

    print("\nGen 1")
    for p in population:
        print("Tower")
        p.print_pieces()

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
        #TODO: Never seems to end
        start_time = time.time()
        file_data = numbers2arr(file_name)
        population = bucket_distributor(file_data)
        best_one = population.copy()
        while (time.time() - start_time) < problem_time:
            population = p1_genetic_solver(population)
            if scoring(population) > scoring(best_one):
                best_one = population.copy()
        print("Best list is :")
        print(best_one)
        print("With a score of %f " % scoring(best_one))


    elif(puzzle_id == 2):
        #Run Tower Builder Puzzle
        start_time = time.time()
        #while (time.time() - start_time) < problem_time:
        p2_tower_building(file_name)

    else:
        print("Incorrect Puzzle Identifier")
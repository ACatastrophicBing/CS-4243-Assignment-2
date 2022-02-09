import random
import numpy

def main():
    count = 40
    numbers = []

    infile = open ('p1_testing.txt', 'w')

    for n in range(1,count):
        numbers.append(round(random.uniform(-10.0, 10.0), 1))
    infile.write('\n'.join(map(str, numbers)))
    infile.close()
main()
#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import random
import operator
import time
import matplotlib.pyplot as plt

temps1 = time.time()

import floor_plan
import tiles



class Camera(object):
    def __init__(self, position_x = 0, position_y=0, orientation=0):
        self.position_x = position_x
        self.position_y = position_y
        self.orientation = orientation


# genetic algorithm function
score = 0

#def fitness(target_area, individual):
#    temp_area = ((individual.position_x + individual.position_y) / individual.orientation)
#    score = temp_area / target_area
#    return score

def fitness(target_area, individual):
    plan.cameras = individual
    plan.mark_all_cameras(tracer)
    return plan.get_coverage()


def generatePosition():
    part = Camera
    part.position_x = random.uniform(0, 100)
    part.position_y = random.uniform(0, 100)
    part.orientation = random.uniform(0, 6.28)
    return part


def generateIndividual(number_of_cameras):
    individual = [generatePosition() for _ in range(number_of_cameras)]
    return individual


def generateFirstPopulation(sizePopulation, number_of_cameras):
    population = [generateIndividual(number_of_cameras) for _ in range(sizePopulation)]
    return population

#def generateFirstPopulation(sizePopulation):
#    population = []
#    i = 0
#    while i < sizePopulation:
#        population.append(generatePosition())
#        i += 1
#    return population


def computePerfPopulation(population, target_area):
    populationPerf = {}
    for temp_area in population:
        populationPerf[temp_area] = fitness(target_area, temp_area)
    return sorted(populationPerf.items(), key=operator.itemgetter(1), reverse=True)


def selectFromPopulation(populationSorted, best_sample, lucky_few):
    nextGeneration = []
    for i in range(best_sample):
        nextGeneration.append(populationSorted[i][0])
    for i in range(lucky_few):
        nextGeneration.append(random.choice(populationSorted)[0])
    random.shuffle(nextGeneration)
    return nextGeneration


def createChild(individual1, individual2):
    child = 0
    for i in range(len(individual1)):
        if (int(100 * random.random()) < 50):
            child += individual1[i]
        else:
            child += individual2[i]
    return child


def createChildren(breeders, number_of_child):
    nextPopulation = []
    for i in range(len(breeders) // 2):
        for j in range(number_of_child):
            nextPopulation.append(createChild(breeders[i], breeders[len(breeders) - 1 - i]))
    return nextPopulation


def mutatePosition(position):
    position.position_x += 1
    position.position_y += 1
    position.orientation += 0.1

    return position


def mutatePopulation(population, chance_of_mutation):
    for i in range(len(population)):
        if random.random() * 100 < chance_of_mutation:
            population[i] = mutatePosition(population[i])
    return population


def nextGeneration(firstGeneration, target_area, best_sample, lucky_few, number_of_child, chance_of_mutation):
    populationSorted = computePerfPopulation(firstGeneration, target_area)
    nextBreeders = selectFromPopulation(populationSorted, best_sample, lucky_few)
    nextPopulation = createChildren(nextBreeders, number_of_child)
    nextGeneration = mutatePopulation(nextPopulation, chance_of_mutation)
    return nextGeneration


def multipleGeneration(number_of_generation, target_area, number_of_cameras, size_population, best_sample, lucky_few, number_of_child,
                       chance_of_mutation):
    historic = []
    historic.append(generateFirstPopulation(size_population, number_of_cameras))
    for i in range(number_of_generation):
        historic.append(
            nextGeneration(historic[i], target_area, best_sample, lucky_few, number_of_child, chance_of_mutation))
    return historic


# print result:
def printSimpleResult(historic, target_area, number_of_generation):  # bestSolution in historic. Caution not the last
    result = getListBestIndividualFromHistorique(historic, target_area)[number_of_generation - 1]
    print("solution: \"" + result[0] + "\" de fitness: " + str(result[1]))


# analysis tools
def getBestIndividualFromPopulation(population, target_area):
    return computePerfPopulation(population, target_area)[0]


def getListBestIndividualFromHistorique(historic, target_area):
    bestIndividuals = []
    for population in historic:
        bestIndividuals.append(getBestIndividualFromPopulation(population, target_area))
    return bestIndividuals


# graph
def evolutionBestFitness(historic, target_area):
    plt.axis([0, len(historic), 0, 105])
    plt.title(target_area)

    evolutionFitness = []
    for population in historic:
        evolutionFitness.append(getBestIndividualFromPopulation(population, target_area)[1])
    plt.plot(evolutionFitness)
    plt.ylabel('fitness best individual')
    plt.xlabel('generation')
    plt.show()


def evolutionAverageFitness(historic, target_area, size_population):
    plt.axis([0, len(historic), 0, 105])
    plt.title(target_area)

    evolutionFitness = []
    for population in historic:
        populationPerf = computePerfPopulation(population, target_area)
        averageFitness = 0
        for individual in populationPerf:
            averageFitness += individual[1]
        evolutionFitness.append(averageFitness / size_population)
    plt.plot(evolutionFitness)
    plt.ylabel('Average fitness')
    plt.xlabel('generation')
    plt.show()


# variables
target_area = 100
temp_area = 0
number_of_cameras = 20
size_population = 100
best_sample = 20
lucky_few = 20
number_of_child = 5
number_of_generation = 100
chance_of_mutation = 0

# program
if ((best_sample + lucky_few) / 2 * number_of_child != size_population):
    print("population size not stable")
else:
    [grid, corners] = floor_plan.floor_loader.load_map('../pictures/mapa.png',
                                                       '../pictures/mapa.txt')
    plan = floor_plan.FloorPlan(grid, corners)

    tracer = floor_plan.ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)

    historic = multipleGeneration(number_of_generation, target_area, number_of_cameras, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation)

    printSimpleResult(historic, target_area, number_of_generation)

    evolutionBestFitness(historic, target_area)
    evolutionAverageFitness(historic, target_area, size_population)

    print(time.time() - temps1)
    print(historic)
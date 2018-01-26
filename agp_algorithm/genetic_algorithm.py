#!/usr/bin/python3.5
# -*-coding:Utf-8 -*

import random
import operator
import time
import matplotlib.pyplot as plt

temps1 = time.time()

import floor_plan
import tiles
from camera import Camera


def fitness(target_area, individual):
    plan.cameras = individual
    plan.mark_all_cameras(tracer)
    return plan.get_coverage()


from random import randint

def generatePosition():
    part = Camera()
    part.position[0] = randint(10, 220)
    part.position[1] = randint(10, 220)
    part.orientation = random.uniform(0, 2*3.14)

    return part


def generateIndividual(number_of_cameras):
    individual = [generatePosition() for _ in range(number_of_cameras)]
    return individual


def generateFirstPopulation(sizePopulation, number_of_cameras):
    population = [generateIndividual(number_of_cameras) for _ in range(sizePopulation)]
    return population


class Population(object):
    def __init__(self, camera=None, total_area = 0):
        self.camera = [Camera() for _ in range(20)]
        self.total_area = total_area


def computePerfPopulation(population, target_area):
    populationPerf = [Population() for _ in range(100)]
    i = 0
    #populationPerf = [list(individual) for individual in set(fitness(target_area, individual) for individual in population)]
    for individual in population:
        populationPerf[i].camera = individual
        populationPerf[i].total_area = fitness(target_area, individual)
        i += 1
    return sorted(populationPerf, key=operator.attrgetter('total_area'), reverse=True)


def selectFromPopulation(populationSorted, best_sample, lucky_few):
    nextGeneration = []
    for i in range(best_sample):
        nextGeneration.append(populationSorted[i])
    for i in range(lucky_few):
        nextGeneration.append(random.choice(populationSorted))
    random.shuffle(nextGeneration)
    return nextGeneration


def createChild(individual1, individual2):
    child = [Camera for _ in range(20)]
    for i in range(20):
        if (int(100 * random.random()) < 50):
            child[i] = individual1.camera[i]
        else:
            child[i] = individual2.camera[i]
    return child


def createChildren(breeders, number_of_child):
    nextPopulation = []
    for i in range(len(breeders) // 2):
        for j in range(number_of_child):
            nextPopulation.append(createChild(breeders[i], breeders[len(breeders) - 1 - i]))
    return nextPopulation


def mutatePosition(position):
    for individual in position:
        individual.position[0] += 1
        individual.position[1] += 1
        individual.orientation += 1

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
    print("Cameras positions:\r\n")
    i = 0
    for individual in result.camera:
        print(" " + individual.position)
        i += 1
    print("Total area: " + result.total_area)


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
target_area = 0.9
temp_area = 0
number_of_cameras = 20
size_population = 50
best_sample = 10
lucky_few = 10
number_of_child = 5
number_of_generation = 30
chance_of_mutation = 0

# program
if ((best_sample + lucky_few) / 2 * number_of_child != size_population):
    print("population size not stable")
else:
    [grid, corners] = floor_plan.floor_loader.load_map('../pictures/mapa.png',
                                                       '../pictures/mapa.txt')
    plan = floor_plan.FloorPlan(grid, corners)

    tracer = floor_plan.ray_trace.RayTrace(tiles.occupied_tiles, tiles.Tiles.SEEN, False)
    plan.cameras = [Camera([0, 0], 0.0, 1 * 3.14 / 2.0, range_of_view=20.0)]
    historic = multipleGeneration(number_of_generation, target_area, number_of_cameras, size_population, best_sample, lucky_few, number_of_child, chance_of_mutation)

    printSimpleResult(historic, target_area, number_of_generation)

    evolutionBestFitness(historic, target_area)
    evolutionAverageFitness(historic, target_area, size_population)

    print(time.time() - temps1)
    print(historic)
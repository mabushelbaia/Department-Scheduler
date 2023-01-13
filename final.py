import copy
from Course import *
from typing import *
import time
import random


Population = list[Chromosome]


def generate_population(size: int) -> Population:
    population = []
    while True:
        schedule = Chromosome(None)
        if schedule.fitness:
            population.append(schedule)
        if len(population) == size:
            break
    return population


def selection(population: Population, k: int) -> Population:
    ranks_sum = len(population) * (len(population) + 1) / 2
    population.sort(key=lambda x: x.fitness, reverse=True)
    return random.choices(population, weights=[(len(population) - i) / ranks_sum for i in range(len(population))], k=k)


def crossover(parent1: Chromosome, parent2: Chromosome) -> Population:
    Parent1, Parent2 = copy.deepcopy(
        parent1.courses), copy.deepcopy(parent2.courses)
    single_crossover_point = random.randint(1, len(Parent1) - 1)
    double_crossover_point = random.randint(1, len(Parent2) - 1)
    if single_crossover_point > double_crossover_point:
        single_crossover_point, double_crossover_point = double_crossover_point, single_crossover_point
    Child1 = Parent1[:single_crossover_point] + \
        Parent2[single_crossover_point:double_crossover_point] + \
        Parent1[double_crossover_point:]
    Child2 = Parent2[:single_crossover_point] + \
        Parent1[single_crossover_point:double_crossover_point] + \
        Parent2[double_crossover_point:]
    Child1 = Chromosome(Child1)
    Child2 = Chromosome(Child2)
    return Child1 if Child1.fitness else parent1, Child2 if Child2.fitness else parent2


def mutation(chromosome: Chromosome, mutation_rate: float):
    mutated_chromosome = copy.deepcopy(chromosome.courses)
    if random.random() < mutation_rate:
        for _ in range(10):  # 10 attempts to mutate
            course = random.randint(
                10, len(mutated_chromosome) - 1)  # random course
            if mutated_chromosome[course][1] == "Lecture":
                section = random.randint(
                    0, len(mutated_chromosome[course][2]) - 1)  # random section
                mutated_chromosome[course][2][section][1] = random.choice(
                    lecture_slots)
            else:
                section = random.randint(
                    0, len(mutated_chromosome[course][2]) - 1)  # random section
                mutated_chromosome[course][2][section][1] = random.choice(
                    lab_slots)  # mutate
            mutated_chromosome = Chromosome(mutated_chromosome)
            if mutated_chromosome.fitness:  # if mutation is valid
                return mutated_chromosome
            mutated_chromosome = mutated_chromosome.courses
    return chromosome


def run_ga(initial_population: int, mutation_rate: float, generations: int, size: int) -> Population:
    population = generate_population(initial_population)
    population.sort(key=lambda x: x.fitness, reverse=True)
    print("Initial Fitness Range: ", round(population[-1].fitness, 2), round(population[0].fitness, 2))
    print("Initial Conflicts: ", population[0].conflict_sum)
    print("Initial Early Slots: ", population[0].early_penalty, "Late Slots: ",
          population[0].late_penalty, "Saturday Slots: ", population[0].saturday_penalty)
    print("Initial Sequential Lectures: ", population[0].sequenctial_pelanty)
    start = time.time()
    for j in range(generations):
        population = population[:size]
        for i in range(int(len(population)//2)):
            parents = selection(population, 2)
            offspring = crossover(parents[0], parents[1])
            offspring = [mutation(offspring[0], mutation_rate), mutation(
                offspring[1], mutation_rate)]
            population.extend(offspring)
        # print(f"Fitness {j}: ", ", ".join([str(round(x.fitness,3)) for x in population[:5]]))
        population.sort(key=lambda x: x.fitness, reverse=True)
    print("="*50)
    print("Fitness {Range}: ", round(
        population[-1].fitness, 2), round(population[0].fitness, 2))
    print("Conflicts: ", population[0].conflict_sum)
    print("Early Slots: ", population[0].early_penalty, "Late Slots: ",
          population[0].late_penalty, "Saturday Slots: ", population[0].saturday_penalty)
    print("Sequential Lectures: ", population[0].sequenctial_pelanty)
    print("Time taken: ", time.time() - start)
    print("Top 5: ", ", ".join([str(x.fitness) for x in population[:5]]))
    print("Schedule: ")
    print_schedule(population[0])
    with open("schedule.txt", "w") as f:
        f.write(str(population[0].courses))
run_ga(initial_population=100, mutation_rate=0.3, generations=1000, size=100)

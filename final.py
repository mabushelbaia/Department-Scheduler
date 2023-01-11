import copy
from Course import *
from typing import List, Tuple
import time
import random

Gene = list
Chromosome = list[Gene]
Population = list[Chromosome]

def generate_chromosome(courses: list[Course]) -> Chromosome:
    schedule = []
    for course in courses:
        gene = [course.year, course.type]
        if course.type == "Lecture":
            sections = random.choices(lecture_slots, k=course.sections)
        else:
            sections = random.sample(lab_slots, k=course.sections)
        l = []
        for key, value in course.teachers.items():
            l.extend([key] * value)
        sections = list(map(list, zip(l, sections)))
        gene.append(sections)
        schedule.append(gene)
    return schedule

def generate_population(size: int, courses: list) -> Population:
    population = []
    for _ in range(size):
        x = generate_chromosome(courses)
        if fitness(x)[0] != 0:
            population.append(x) 
    return population


def fitness(schedule: Chromosome) -> float:
    score = 0 
    teacher_slots = {}
    unique_slots = set()          
    early_penalty = 0
    late_penalty = 0
    saturday_penalty = 0
    conflicts = {2: {}, 3: {}, 4: {}, 5: {}}
    if schedule is None:
        return 0, 0, 0
    for course in schedule:
        local_lab_slots = {} # For checking lab conflicts
        local_days = {} 
        local_slots = set()  
        for (teacher, slot) in course[2]:
            if teacher in teacher_slots:
                if slot in teacher_slots[teacher]:
                    return -300, 0, 0
                else:
                    teacher_slots[teacher].append(slot)
            else:
                teacher_slots[teacher] = [slot]
            if course[1] == "Lab":
                if slot in local_lab_slots:
                    return -300, 0, 0
                else:
                    local_lab_slots[slot] = True
            if course[1] == "Lab":
                local_days[slot[0]] = local_days.get(slot[0], 0) + 1
            elif course[1] == "Lecture":
                local_days[slot[0]] = local_days.get(slot[0], 0) + 1
                local_days[slot[1]] = local_days.get(slot[1], 0) + 1
            if slot[-1] in ["08:30 - 9:45", "08:30 - 11:10"]:
                    early_penalty += 1
            if slot[-1] == "14:15 - 16:55":
                late_penalty += 1
            if slot[0] == "S":
                saturday_penalty += 1
            conflicts[course[0]][slot] = conflicts[course[0]].get(slot, 0) + 1
            local_slots.add(slot)
            unique_slots.add(slot)
        score += len(local_slots) / len(course[2]) # How many slots does a course cover relative to it section count
        score += len(local_days) / len(course[2])  # How many days does a course cover relative to it section count
    score /= len(schedule) 
    score += 200
    conflict_sum = 0
    for conflict in conflicts.values():
        for value in conflict.values():
            conflict_sum += value - 1
    score -= conflict_sum
    score -= 0.5*early_penalty + 0.5*late_penalty + 0.5*saturday_penalty
    ratio = len(unique_slots) / len(lab_slots + lecture_slots)
    score *= ratio
    return score, lab_slots, conflict_sum

def selection(population: Population, k: int) -> Population:
    ranks_sum = len(population) * (len(population) + 1) / 2
    population = sorted(population, key=lambda x: fitness(x)[0], reverse=True)
    return random.choices(population, weights=[(len(population) - i) / ranks_sum for i in range(len(population))], k=k)


def crossover(parent1: Chromosome, parent2: Chromosome) -> Population:
    Parent1, Parent2  = copy.deepcopy(parent1), copy.deepcopy(parent2)
    single_crossover_point = random.randint(1, len(parent1) - 1)
    Child1 = Parent1[:single_crossover_point] + Parent2[single_crossover_point:]
    Child2 = Parent2[:single_crossover_point] + Parent1[single_crossover_point:]
    return Child1, Child2
def mutation(chromosome: Chromosome, mutation_rate: float):
    mutated_chromosome = copy.deepcopy(chromosome)
    if random.random() < mutation_rate:
        for _ in range(10):  # 10 attempts to mutate
            course = random.randint(0, len(mutated_chromosome) - 1) # random course
            if mutated_chromosome[course][1] == "Lecture": 
                section = random.randint(0, len(mutated_chromosome[course][2]) - 1) # random section
                mutated_chromosome[course][2][section][1] = random.choice(lecture_slots) # mutate
                # print("Mutated Lecture Section "+str(section)+" of "+ courses[course].name)
            else:
                section = random.randint(0, len(mutated_chromosome[course][2]) - 1) # random section
                mutated_chromosome[course][2][section][1] = random.choice(lab_slots) # mutate
            if fitness(mutated_chromosome)[0] > 0: # if mutation is valid
                return mutated_chromosome
    return chromosome

def run_ga(initial_population:int, mutation_rate: float, generations: int, size: int) -> Population:
    population = generate_population(initial_population, courses)
    best_random = sorted(population, key=lambda x: fitness(x)[0], reverse=True)[0]
    x = fitness(best_random) 
    print(x[0], x[2])
    start = time.time()
    for _ in range(generations):
        population.sort(key=lambda x: fitness(x)[0], reverse=True)
        population = population[:size]
        #print([fitness(x)[0] for x in population])
        for _ in range(int(len(population) * 0.8)):
            parents = selection(population, 2)
            offspring = crossover(parents[0], parents[1])
            offspring = [mutation(offspring[0], mutation_rate), mutation(offspring[1], mutation_rate)]
            population.extend(offspring)
        print([fitness(x)[0] for x in population])
    population.sort(key=lambda x: fitness(x)[0], reverse=True)
    print("Schedule: ")
    print_schedule(population[0])
    print("Fitness: ", fitness(population[0])[0], fitness(population[0])[2])
    print("Time taken: ", time.time() - start)

    print("Top 5: ", ",".join([str(fitness(x)[0]) for x in population[:5]]))

        
run_ga(50_000, 0.1, 1000, 10)

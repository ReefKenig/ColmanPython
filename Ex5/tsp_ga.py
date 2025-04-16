import random
import math


def solve(points: list) -> list:
    POP_SIZE = 100
    GENERATIONS = 500
    MUTATION_RATE = 0.05

    # Euclidean distance
    def dist(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    # Calculate total path distance
    def fitness(path):
        return sum(dist(path[i], path[i+1]) for i in range(len(path) - 1)) + dist(path[-1], path[0]) # Return to start

    # Generate a random path
    def create_individual():
        individual = points[:]
        random.shuffle(individual)
        return individual

    # Crossover between two parents
    def crossover(parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child_p1 = parent1[start:end]
        child = child_p1 + [city for city in parent2 if city not in child_p1]
        return child

    # Mutate a path by swapping two cities
    def mutate(path):
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(path)), 2)
            path[i], path[j] = path[j], path[i]

    # Initial population
    population = [create_individual() for _ in range(POP_SIZE)]

    # Evolution loop
    for _ in range(GENERATIONS):
        population.sort(key=fitness) # Sort by path length
        new_population = population[:10] # Elitism: keep top 10

        # Fill rest of population
        while len(new_population) < POP_SIZE:
            parent1, parent2 = random.choices(population[:50], k=2) # Tournament selection
            child = crossover(parent1, parent2)
            mutate(child)
            new_population.append(child)

        population = new_population

    # Return the best path found
    return population[0]
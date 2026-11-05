import random
import math

# Cities: (x, y) coordinates
cities = [(0, 0), (2, 3), (5, 2), (6, 6), (8, 3)]

POP_SIZE = 10
GENERATIONS = 100
MUTATION_RATE = 0.1


# Calculate distance between two cities
def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# Calculate total distance of a route
def fitness(route):
    total = 0
    for i in range(len(route)):
        total += distance(cities[route[i]],
                          cities[route[(i + 1) % len(route)]])
    return total


# Create initial population
population = []

for _ in range(POP_SIZE):
    route = list(range(len(cities)))
    random.shuffle(route)
    population.append(route)


# Genetic Algorithm
for generation in range(GENERATIONS):

    # Sort routes by distance (shortest = best)
    population.sort(key=fitness)

    # Keep the best route
    new_population = [population[0]]

    while len(new_population) < POP_SIZE:

        # Select two parents
        parent1, parent2 = random.sample(population[:5], 2)

        # Simple crossover
        start, end = sorted(random.sample(range(len(cities)), 2))
        child = [-1] * len(cities)

        child[start:end] = parent1[start:end]

        remaining = [x for x in parent2 if x not in child]

        j = 0
        for i in range(len(child)):
            if child[i] == -1:
                child[i] = remaining[j]
                j += 1

        # Mutation: swap two cities
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(cities)), 2)
            child[i], child[j] = child[j], child[i]

        new_population.append(child)

    population = new_population


# Best solution
best_route = min(population, key=fitness)

print("Best Route:", best_route)
print("Minimum Distance:", round(fitness(best_route), 2))
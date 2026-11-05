import random
import matplotlib.pyplot as plt

def aco_tsp(distance, ants=20, iterations=100, alpha=1, beta=5, rho=0.5):
    n = len(distance)
    pheromone = [[1.0] * n for _ in range(n)]

    best_route = None
    best_distance = float("inf")

    for _ in range(iterations):
        routes = []

        for _ in range(ants):
            route = [0]
            unvisited = set(range(1, n))

            while unvisited:
                current = route[-1]
                choices = []

                for city in unvisited:
                    closeness = 1 / distance[current][city]
                    value = (pheromone[current][city] ** alpha) * \
                            (closeness ** beta)
                    choices.append((city, value))

                total = sum(value for city, value in choices)
                r = random.random() * total
                cumulative = 0

                for city, value in choices:
                    cumulative += value
                    if cumulative >= r:
                        next_city = city
                        break

                route.append(next_city)
                unvisited.remove(next_city)

            route.append(0)

            total_distance = sum(
                distance[route[i]][route[i + 1]]
                for i in range(len(route) - 1)
            )

            routes.append((route, total_distance))

            if total_distance < best_distance:
                best_distance = total_distance
                best_route = route[:]

        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - rho)

        for route, total_distance in routes:
            added = 1 / total_distance

            for i in range(len(route) - 1):
                a = route[i]
                b = route[i + 1]
                pheromone[a][b] += added
                pheromone[b][a] += added

    return best_route, best_distance


n = int(input("Enter number of cities: "))

distance = []

for _ in range(n):
    distance.append(list(map(float, input().split())))

route, best_distance = aco_tsp(distance)

print("Best route:", " -> ".join(map(str, route)))
print("Shortest distance:", best_distance)

x = []
y = []

for city in range(n):
    angle = 2 * 3.14159 * city / n
    x.append(__import__("math").cos(angle))
    y.append(__import__("math").sin(angle))

plt.figure(figsize=(7, 7))

for i in range(len(route) - 1):
    a = route[i]
    b = route[i + 1]

    plt.plot([x[a], x[b]], [y[a], y[b]], marker="o")

for i in range(n):
    plt.text(x[i], y[i], " City " + str(i), fontsize=12)

plt.title("ACO - Best TSP Route")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid()
plt.show()
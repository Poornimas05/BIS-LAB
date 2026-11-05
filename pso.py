import random
def fitness(x):
    return -(x - 5) ** 2 + 100

particles = []

for i in range(5):
    position = random.uniform(0, 10)
    velocity = random.uniform(-1, 1)

    particles.append({
        "position": position,
        "velocity": velocity,
        "pbest": position,
        "pbest_fitness": fitness(position)
    })


gbest = max(particles, key=lambda p: p["pbest_fitness"])
gbest_position = gbest["pbest"]
gbest_fitness = gbest["pbest_fitness"]

w = 0.5
c1 = 1.5
c2 = 1.5

for iteration in range(20):

    for particle in particles:

       
        r1 = random.random()
        r2 = random.random()

        
        particle["velocity"] = (
            w * particle["velocity"]
            + c1 * r1 * (particle["pbest"] - particle["position"])
            + c2 * r2 * (gbest_position - particle["position"])
        )

       
        particle["position"] += particle["velocity"]

        current_fitness = fitness(particle["position"])

        if current_fitness > particle["pbest_fitness"]:
            particle["pbest"] = particle["position"]
            particle["pbest_fitness"] = current_fitness

        if current_fitness > gbest_fitness:
            gbest_position = particle["position"]
            gbest_fitness = current_fitness


print("Best position:", gbest_position)
print("Best fitness:", gbest_fitness)
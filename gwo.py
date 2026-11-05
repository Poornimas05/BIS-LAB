
import random
import math

# 1. Take dataset input
rows = int(input("Enter number of rows: "))
features = int(input("Enter number of features: "))

X = []

for i in range(rows):
    row = list(map(float, input(
        f"Enter row {i+1}: "
    ).split()))

    if len(row) != features:
        raise ValueError("Incorrect number of features")

    X.append(row)

y = input("Enter class labels separated by space: ").split()

if len(y) != rows:
    raise ValueError("Number of labels must match rows")

# 2. Initialize wolves
N = 5
T = 20

wolves = [
    [random.uniform(-6, 6) for _ in range(features)]
    for _ in range(N)
]

# 3. Sigmoid function
def sigmoid(x):
    x = max(-50, min(50, x))
    return 1 / (1 + math.exp(-x))


# 4. Convert position into binary
def binary_position(position):

    mask = []

    for value in position:
        if random.random() < sigmoid(value):
            mask.append(1)
        else:
            mask.append(0)

    if sum(mask) == 0:
        mask[position.index(max(position))] = 1

    return mask


# 5. Calculate classification error
def classification_error(mask):

    selected = [j for j in range(features) if mask[j] == 1]

    correct = 0

    for i in range(rows):

        distances = []

        for k in range(rows):

            if i == k:
                continue

            distance = sum(
                (X[i][j] - X[k][j]) ** 2
                for j in selected
            )

            distances.append((distance, y[k]))

        predicted = min(distances)[1]

        if predicted == y[i]:
            correct += 1

    return 1 - correct / rows


# 6. Evaluate two objectives
def evaluate(position):

    mask = binary_position(position)

    f1 = sum(mask) / features
    f2 = classification_error(mask)

    return (f1, f2, mask)


# 7. Pareto dominance
def dominates(a, b):

    return (
        a[0] <= b[0] and
        a[1] <= b[1] and
        (a[0] < b[0] or a[1] < b[1])
    )


# 8. Find non-dominated solutions
def pareto_sort(solutions):

    result = []

    for i in range(len(solutions)):

        dominated = False

        for j in range(len(solutions)):

            if i != j and dominates(
                solutions[j], solutions[i]
            ):
                dominated = True
                break

        if not dominated:
            result.append(solutions[i])

    return result


# 9. Main GWO algorithm
archive = []

for t in range(T):

    population = []

    for wolf in wolves:

        f1, f2, mask = evaluate(wolf)

        population.append(
            (f1, f2, mask, wolf[:])
        )

    archive = pareto_sort(archive + population)

    # Select three leaders
    leaders = random.sample(
        archive, min(3, len(archive))
    )

    while len(leaders) < 3:
        leaders.append(leaders[0])

    alpha = leaders[0][3]
    beta = leaders[1][3]
    delta = leaders[2][3]

    # Calculate coefficient
    a = 2 - 2 * t / T

    # Update wolf positions
    for i in range(N):

        new_position = []

        for j in range(features):

            A1 = 2*a*random.random() - a
            C1 = 2*random.random()

            A2 = 2*a*random.random() - a
            C2 = 2*random.random()

            A3 = 2*a*random.random() - a
            C3 = 2*random.random()

            D1 = abs(C1*alpha[j] - wolves[i][j])
            D2 = abs(C2*beta[j] - wolves[i][j])
            D3 = abs(C3*delta[j] - wolves[i][j])

            X1 = alpha[j] - A1*D1
            X2 = beta[j] - A2*D2
            X3 = delta[j] - A3*D3

            new_value = (X1 + X2 + X3) / 3

            new_position.append(
                max(-6, min(6, new_value))
            )

        wolves[i] = new_position


# 10. Final evaluation
for wolf in wolves:

    f1, f2, mask = evaluate(wolf)

    archive.append((f1, f2, mask, wolf[:]))

archive = pareto_sort(archive)

# Select one balanced solution
best = min(
    archive,
    key=lambda s: s[0] + s[1]
)

# 11. Simple output
print("\n--- GWO FEATURE SELECTION ---")

print("Selected Features:")

for i in range(features):
    if best[2][i] == 1:
        print("F", i+1)

print("Total Features:", features)
print("Selected Features:", sum(best[2]))
print("Accuracy:", round((1-best[1])*100, 2), "%")
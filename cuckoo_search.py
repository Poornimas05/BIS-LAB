import cv2
import random
import matplotlib.pyplot as plt
import urllib.request

# Step 1: Download a random colour image
url = "https://picsum.photos/300"
urllib.request.urlretrieve(url, "random.jpg")

# Step 2: Read colour image
img = cv2.imread("random.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Step 3: Fitness function
def fitness(params):
    alpha, beta = params
    result = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return result.std()

# Step 4: Create random nests
nests = [
    (random.uniform(0.5, 2.0), random.randint(-80, 80))
    for _ in range(5)
]

# Step 5: Search for better solutions
for _ in range(20):
    for i in range(len(nests)):
        alpha, beta = nests[i]

        new = (
            max(0.5, min(2.0, alpha + random.uniform(-0.3, 0.3))),
            max(-80, min(80, beta + random.randint(-20, 20)))
        )

        if fitness(new) > fitness(nests[i]):
            nests[i] = new

# Step 6: Find best nest
best = max(nests, key=fitness)

# Step 7: Enhance colour image
result = cv2.convertScaleAbs(
    img, alpha=best[0], beta=best[1]
)

# Step 8: Display images
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(img)
plt.title("Original Colour Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result)
plt.title("Enhanced Colour Image")
plt.axis("off")

plt.show()

print("Best contrast:", best[0])
print("Best brightness:", best[1])
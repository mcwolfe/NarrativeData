import random
import numpy as np
import matplotlib.pyplot as plt

# Grid settings
WIDTH, HEIGHT = 50, 50
WALL_PROBABILITY = 0.55  # Initial probability of a cell being a wall
ITERATIONS = 4  # Number of cellular automata generations

# Initialize the grid randomly with walls and open spaces
def initialize_grid(width, height, wall_prob):
    return np.random.choice([0, 1], size=(height, width), p=[1 - wall_prob, wall_prob])

# Count the number of neighboring walls around a cell
def count_neighbors(grid, x, y):
    neighbors = [
        (1, 0), (-1, 0), (0, 1), (0, -1),  # Cardinal directions
        (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal directions
    ]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid.shape[1] and 0 <= ny < grid.shape[0]:
            count += grid[ny, nx]
    return count

# Apply cellular automata rules to evolve the grid
def evolve_grid(grid):
    new_grid = np.copy(grid)
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            wall_neighbors = count_neighbors(grid, x, y)
            if grid[y, x] == 1:  # Cell is a wall
                if wall_neighbors < 4:
                    new_grid[y, x] = 0  # Becomes open
            else:  # Cell is open
                if wall_neighbors > 5:
                    new_grid[y, x] = 1  # Becomes wall
    return new_grid

# Create and evolve the dungeon
grid = initialize_grid(WIDTH, HEIGHT, WALL_PROBABILITY)
for _ in range(ITERATIONS):
    grid = evolve_grid(grid)

# Plot the resulting dungeon
plt.imshow(grid, cmap='binary')
plt.title("Cellular Automata Dungeon")
plt.show()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import lil_matrix

size = 101
grid = np.zeros((size, size, size)) #creating a 3d grid map of size 101x101x101

np.random.seed(29)  
weighted_points = 1000
weighted_coordinates = np.random.choice(size**3, weighted_points, replace=False)
weights = np.random.rand(weighted_points) * 10  
grid.flat[weighted_coordinates] = weights

#input start and goal coordinates
sets = [
    {"start": (0, 0, 0), "end": (98, 80, 79)},
    {"start": (0, 0, 0), "end": (89, 79, 50)},
]

def get_oneD_coordinate(x, y, z):
    return x * size**2 + y * size + z  #flattening a 3d coordinate to 1d coordinate


def get_threeD_coordinates(index): #getting the 3d coordinate from 1d coordinate
    x = index // (size**2)
    y = (index % (size**2)) // size
    z = index % size
    return x, y, z


def create_graph(grid):
    total_size = size**3
    graph = lil_matrix((total_size, total_size), dtype=np.float64)  # Sparse matrix for adjacency
    for x in range(size):
        for y in range(size):
            for z in range(size):
                current_index = get_oneD_coordinate(x, y, z)
                for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < size and 0 <= ny < size and 0 <= nz < size:
                        neighbor_index = get_oneD_coordinate(nx, ny, nz)
                        graph[current_index, neighbor_index] = grid[nx, ny, nz] + 1  # Add 1 to avoid zero weights
    return graph.tocsr()  # Convert list of lists (LIL) format to a Compressed Sparse Row (CSR) format.


graph = create_graph(grid)

paths = []
for s in sets:
    start_index = get_oneD_coordinate(*s["start"])
    end_index = get_oneD_coordinate(*s["end"])
    dist_matrix, predecessors = dijkstra(graph, indices=start_index, return_predecessors=True)
    path = []
    current_index = end_index
    while current_index != start_index:
        path.append(get_threeD_coordinates(current_index))
        current_index = predecessors[current_index]
    path.append(get_threeD_coordinates(start_index))
    path.reverse()
    paths.append(path)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

colors = ['r', 'g']
for i, path in enumerate(paths):
    x, y, z = zip(*path)
    ax.plot(x, y, z, color=colors[i], label=f'Path {i+1}')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()


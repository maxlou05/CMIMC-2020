import math
import matplotlib.pyplot as plt
import numpy as np
import sys

TASK_NUM = int(sys.argv[1])    # These are command line arguments, so when running, type: program.py arg1 arg2 ...
RESOLUTION = int(sys.argv[2])  # Note that its a space, -o is called options
LOCALITY = float(sys.argv[3])
EXPANSION = float(sys.argv[4])

f = open('D:\Programs\Python programs\CMIMC\circlecovers{}.txt'.format(TASK_NUM), 'r')

n = int(f.readline())
points = [(f.readline()).split() for _ in range(n)]
tx = []
ty = []
for i in points:
    tx.append (int(i[0]))
    ty.append (int(i[1]))

pts_x = np.array(tx)
pts_y = np.array(ty)

m = int(f.readline())
radii = [int(f.readline()) for _ in range(m)]

centers = []



# Knerel Density Estimation - not mine
dx = max(pts_x) - min(pts_x)
dy = max(pts_y) - min(pts_y)

delta = min(dx, dy) / RESOLUTION
nx = int(dx / delta)
ny = int(dy / delta)
radius = (1 / LOCALITY) * min(dx, dy)

grid_x = np.linspace(min(pts_x), max(pts_x), num=nx)
grid_y = np.linspace(min(pts_y), max(pts_y), num=ny)

x, y = np.meshgrid(grid_x, grid_y)


def gauss(x1, x2, y1, y2):
    """
    Apply a Gaussian kernel estimation (2-sigma) to distance between points.

    Effectively, this applies a Gaussian kernel with a fixed radius to one
    of the points and evaluates it at the value of the euclidean distance
    between the two points (x1, y1) and (x2, y2).
    The Gaussian is transformed to roughly (!) yield 1.0 for distance 0 and
    have the 2-sigma located at radius distance.
    """
    return (
        (1.0 / (2.0 * math.pi))
        * math.exp(
            -1 * (3.0 * math.sqrt((x1 - x2)**2 + (y1 - y2)**2) / radius))**2
        / 0.4)


def _kde(x, y):
    """
    Estimate the kernel density at a given position.

    Simply sums up all the Gaussian kernel values towards all points
    (pts_x, pts_y) from position (x, y).
    """
    return sum([
        gauss(x, px, y, py)
        # math.sqrt((x - px)**2 + (y - py)**2)
        for px, py in zip(pts_x, pts_y)
    ])


kde = np.vectorize(_kde)  # Let numpy care for applying our kde to a vector
z = kde(x, y)

print(z.shape)
zc = np.copy(z)

# Save the density results to use later
zfile = open('z_array{}_LOCALITY{}_RES{}.npy'.format(TASK_NUM, LOCALITY, RESOLUTION), 'wb')
np.save(zfile, z)
zfile.close()



# Finding the points to put the centers
step = 0
stepc = 0
x_lo = 0
x_hi = 0
y_lo = 0
y_hi = 0
x_loc = 0
x_hic = 0
y_loc = 0
y_hic = 0



for c in range(len(radii)):
    xi, yi = np.where(z == np.amax(z))  # Returns the point where the density is highest
    print(xi, yi)

    max_x = grid_x[yi][0]  # For some reason this is reversed, so I un-reversed it by double reversing
    max_y = grid_y[xi][0]
    print(f"{max_x:.4f}, {max_y:.4f}")

    centers.append((max_x, max_y))

    # Drawing graphs
    if c == 0:
        # fig, ax = plt.subplots()
        # ax.scatter(pts_x, pts_y, marker='.', color='blue')
        # ax.scatter(max_x, max_y, marker='+', color='red', s=200)
        # fig.set_size_inches(4, 4)
        # fig.savefig('D:\Programs\Python programs\CMIMC\points{}.png'.format(TASK_NUM), bbox_inches='tight')
        # fig.show()

        fig, ax = plt.subplots()
        ax.pcolormesh(x, y, z, cmap='inferno', vmin=np.min(z), vmax=np.max(z))
        fig.set_size_inches(4, 4)
        fig.savefig('D:\Programs\Python programs\CMIMC\density{}_LOCALITY{}_RES{}.png'.format(TASK_NUM, LOCALITY, RESOLUTION), bbox_inches='tight')
        # fig.show()

    step = math.ceil(radii[c]*EXPANSION/delta)  # EXPANSION is used to determine how much larger the area to not put the center is compared to the circle
    stepc = math.ceil(radii[c]/delta)  # All of the variables with c behind them are just copies and are used for graphing purposes only
    x_lo = xi[0] - step
    x_hi = xi[0] + step
    y_lo = yi[0] - step
    y_hi = yi[0] + step
    x_loc = xi[0] - stepc
    x_hic = xi[0] + stepc
    y_loc = yi[0] - stepc
    y_hic = yi[0] + stepc

    for i in range(x_lo, x_hi+1):
        if i >= z.shape[0]:  #If it's out of the graph/bounds
            continue
        for j in range(y_lo, y_hi+1):
            if j >= z.shape[1]:
                continue
            # print(i,j)
            # Set the density of the approximate area covered by the circle and more to 0 (square with sidelenghth radius*EXPANSION)
            # (it's so that the circles don't overlap as much)
            z[i][j] = 0
            if i >= x_loc and i <= x_hic and j >= y_loc and j <= y_hic:
                zc[i][j] = 0

    # fig, ax = plt.subplots()
    # ax.pcolormesh(x, y, z, cmap='inferno', vmin=np.min(z), vmax=np.max(z))
    # fig.set_size_inches(4, 4)
    # fig.show()

fig, ax = plt.subplots()
ax.pcolormesh(x, y, zc, cmap='inferno', vmin=np.min(z), vmax=np.max(z))
fig.set_size_inches(4, 4)
fig.savefig('D:\Programs\Python programs\CMIMC\density_covered{}_LOCALITY{}_RES{}.png'.format(TASK_NUM, LOCALITY, RESOLUTION), bbox_inches='tight')
# fig.show()

fig, ax = plt.subplots()
ax.pcolormesh(x, y, z, cmap='inferno', vmin=np.min(z), vmax=np.max(z))
fig.set_size_inches(4, 4)
fig.savefig('D:\Programs\Python programs\CMIMC\density_covered_L{}_LOCALITY{}_RES{}.png'.format(TASK_NUM, LOCALITY, RESOLUTION), bbox_inches='tight')

# Writing output file
out = open('D:\Programs\Python programs\CMIMC\CirclesT{}.txt'.format(TASK_NUM), 'w')
for t in range(len(centers)):
    out.write(str(centers[t]).replace(",","").replace("(","").replace(")",""))
    out.write("\n")
out.close()

# input()

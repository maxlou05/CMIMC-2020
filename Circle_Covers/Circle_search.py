import numpy as np
import matplotlib.pyplot as plt
import math
import copy

TASK_NUM = 5
LOCALITY = 100
RESOLUTION = 200  # Just use min(graph.size) to figure out if don't know
MAX_EXPANSION = 2.3
EXP_RES = 13
MOVE_DIST = 100
MOVE_RES = 200

f = open('D:\Programs\Python programs\CMIMC\z_array{}_LOCALITY{}_RES{}.npy'.format(TASK_NUM, LOCALITY, RESOLUTION), 'rb')
# f = open('D:\Programs\z_array1.npy', 'rb')
graph = np.load(f)
f.close()

p = open('D:\Programs\Python programs\CMIMC\circlecovers{}.txt'.format(TASK_NUM), 'r')
n = int(p.readline())
points = [(p.readline()).split() for _ in range(n)]

tpts = []
Dtype = [('x', int), ('y', int)]
for i in points:
    tpts.append((int(i[0]), int(i[1])))

pts = np.array(tpts, dtype=Dtype)
pts = np.sort(pts, order=['x','y'])
ptsc = np.copy(pts)
xmin = pts['x'][0]
xmax = pts['x'][-1]
ymin = min(pts['y'])
ymax = max(pts['y'])

m = int(p.readline())
radii = [int(p.readline()) for _ in range(m)]

p.close()

centers = []



# fig, ax = plt.subplots()
# ax.scatter(pts['x'], pts['y'], marker='.', color='blue')
# fig.set_size_inches(4, 4)
# fig.savefig('D:\Programs\Python programs\CMIMC\points{}.png'.format(TASK_NUM), bbox_inches='tight')
# fig.show()


dx = xmax - xmin
dy = ymax - ymin

delta = min(dx, dy) / RESOLUTION
nx = int(dx / delta)
ny = int(dy / delta)
# radius = (1 / LOCALITY) * min(dx, dy)

grid_x = np.linspace(xmin, xmax, num=nx)
grid_y = np.linspace(ymin, ymax, num=ny)

print(dx, dy, nx, ny, delta)

print(grid_x.shape)
print(grid_y.shape)
# graph = np.delete(graph, [300,301,302], axis=1)
print(graph.shape)
print(pts.shape)
print(LOCALITY)


# Counts how many points the circle at this center covers given:
# rx is x-value of circle's center
# ry is y-value of circle's center
# r is radius of the circle
# p is list of points
def count(rx, ry, r, p):
    score = 0
    pi = []
    length = np.where(np.logical_and(np.logical_and(p['x'] >= rx-r, p['x'] <= rx+r), np.logical_and(p['y'] >= ry-r, p['y'] <= ry+r)))
    for i in length[0]:
        dist = math.sqrt((rx-p['x'][i])**2 + (ry-p['y'][i])**2)
        if dist < r:
            score += 1
            pi.append(i)
    return (score, pi)



espace = np.linspace(1, MAX_EXPANSION, num=EXP_RES)
centers2 = []
bestcenters = []
bestscore = 0
graphc = np.copy(graph)
for i in range(len(radii)):
    centers2.append([0,0,0])

# Testing different values of EXPANSION (e represents EXPANSION)    *see Graph_density.py to see what that means
for e in espace:
    # First test, calculate the original centers score
    totalscore = 0
    centers.clear()
    graphc = np.copy(graph)
    ptsc = np.copy(pts)
    for r in range(len(radii)):
        xi, yi = np.where(graphc == np.amax(graphc))
        max_x = grid_x[yi][0]  # For some reason this is reversed, so I un-reversed it by double reversing.
        max_y = grid_y[xi][0]

        centers.append((max_x, max_y))
        s = count(max_x, max_y, radii[r], ptsc)
        totalscore += s[0]
        centers2[r][0] = max_x
        centers2[r][1] = max_y
        centers2[r][2] = s[0]
        if(len(s[1])>0):
            ptsc = np.delete(ptsc, s[1])
        
        step = math.ceil(radii[r]*e/delta) # As seen, e represents EXPANSION
        x_lo = xi[0] - step
        x_hi = xi[0] + step
        y_lo = yi[0] - step
        y_hi = yi[0] + step

        for i in range(x_lo, x_hi+1):
            if i >= graphc.shape[0]:  #If it's out of the graph/bounds
                continue
            for j in range(y_lo, y_hi+1):
                if j >= graphc.shape[1]:
                    continue
                graphc[i][j] = 0

    
    # Save the scores
    print("-----loop----- score:" + str(totalscore) + ", bestscore:" + str(bestscore)  )

    if totalscore > bestscore:
        # print("-----best 1--------")
        bestscore = totalscore
        bestcenters = copy.deepcopy(centers2)
        # print(bestcenters)
    totalscore = 0
    for b in range(len(radii)):
        centers2[b][0] = 0
        centers2[b][1] = 0
        centers2[b][2] = 0
    ptsc = np.copy(pts)
    
    # Now, move the center around by in an area defined by MOVE_DIST and a resolution defined by MOVE_RES (resolution as in how large each step is)
    for c in range(len(centers)):
        xspace = np.linspace(centers[c][0]-MOVE_DIST, centers[c][0]+MOVE_DIST, num=MOVE_RES)
        yspace = np.linspace(centers[c][1]-MOVE_DIST, centers[c][1]+MOVE_DIST, num=MOVE_RES)
        ptsi = []
        for i in xspace:
            for j in yspace:
                s = count(i, j, radii[c], ptsc)
                if s[0] > centers2[c][2]:  # Save the centers of highest score (for the current EXPANSION value/setting)
                    centers2[c][0] = i
                    centers2[c][1] = j
                    centers2[c][2] = s[0]
                    ptsi = copy.deepcopy(s[1])

        ptsc = np.delete(ptsc, ptsi)
        totalscore += len(ptsi)


    if totalscore > bestscore:
        bestcenters = copy.deepcopy(centers2)
        bestscore = totalscore
        print("-------best--------" + str(bestscore))

print("------------bestscore----------- " + str(bestscore))
# print("-----------bestcenters---------- " + str(bestcenters))

# This is just a final check that calcualtes the score of the best centers again for trouble shooting purposes
totalscore = 0
ptsc = np.copy(pts)
for yay in range(len(radii)):
    s = count(bestcenters[yay][0], bestcenters[yay][1], radii[yay], ptsc)
    totalscore += s[0]
    ptsc = np.delete(ptsc, s[1])
print("---------check----------- " + str(totalscore))
print("--------locality--------- " + str(LOCALITY))

out = open('D:\Programs\Python programs\CMIMC\CirclesT{}_LOCALITY{}.txt'.format(TASK_NUM, LOCALITY), 'w')
for t in range(len(bestcenters)):
    out.write(str(bestcenters[t][0]) + " " + str(bestcenters[t][1]))
    out.write("\n")

out.close()

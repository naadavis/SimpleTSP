# Bounded Search for TSP
from math import sqrt
import matplotlib.pyplot as plt

# Path Length
pLength = 13

# Distance Function
def dist( p1, p2 ):
    return sqrt(sum(map(lambda x: x**2 ,map(lambda x: x[0] - x[1],zip(p1,p2)))))

# Draw A Path
def draw(path):
    plt.clf()
    plt.scatter( list(map(lambda x: x[0], points)),list(map(lambda x: x[1], points)) )
    plt.plot( list(map(lambda x: x[0], path[1])), list(map(lambda x: x[1], path[1])))
    plt.title("Shortest Path: "+str(path[0]))
    plt.axis('square')
    

# Input points
points = []
filename = 'surtlings.txt'
file = open(filename)
for l in file:
    points.append( tuple(map(int,l.split(','))) )
file.close()

if( pLength > len(points) ):
    pLength = len(points)

# Get a Upper Bound for best case with greedy heuristic
# Dicts to track performance
minPerStart = {}    # (start) = (dist,(path))
efficientStart = {} # (start) = (efficiency,(path))

# Greedy NN for each starting point
for pt in points:    # do greedy nn for each starting point
    s = points.copy()
    s.remove(pt)
    path = [pt]
    while len(path) < pLength:
        dlist = list( map( lambda x: dist(x,path[-1]),s))
        nextP = dlist.index( min(dlist) )
        path.append( s.pop(nextP) )
    # compare total distance, update if better
    totalDist = 0
    for i in range(len(path)-1):
        totalDist += dist(path[i],path[i+1])
    if totalDist < minPerStart.get(path[0],(totalDist + 1,))[0]:
        minPerStart[path[0]] = (totalDist,tuple(path))
    # compare and update efficiency
    if totalDist/len(path) < efficientStart.get(path[0],\
                                                (totalDist/len(path)+1,))[0]:
        efficientStart[path[0]] = (totalDist/len(path),tuple(path))

# remember upperbound in form [ length, (path) ]
upperBound = list(min(minPerStart.values(),key=lambda x: x[0]))

# Do DepthFirst Search on entire space recursively, limited by upper bound
# parameters: (),(),int,[]
def boundDepth( currentPath, unexplored, length, upper ):
    # Check Bound
    if currentPath[0] >= upper[0]:  # this path is too long, stop searching this way
        #### DEBUG ####
        #if( len(
        #draw(currentPath)
       # plt.pause(.05)
        ###############
        return
    # Check if Path is long enough to stop, its new shortest
    if len(currentPath[1]) == length:
        print('Found Better: ' + str(currentPath[0]))
        upper[0] = currentPath[0]
        upper[1] = currentPath[1]
        return

    # Otherwise, keep branching
    for p in unexplored:
        newDist = currentPath[0] + dist(p,currentPath[1][-1]) if len(currentPath[1]) > 0 else 0
        newPath = ( newDist, currentPath[1] + (p,) )
        boundDepth( newPath, tuple(x for x in unexplored if x != p), length, upper )

# Find It
boundDepth( (0,()), tuple(points), pLength, upperBound )

##### DEBUG ######
#start = next(x for x in points if x[0] > -2600 and x[1] > 5100)
#plt.figure()
#boundDepth( (0,(start,)), tuple(x for x in points if x != start), pLength, upperBound)
##################

# Draw Best Route
plt.figure()
plt.scatter( list(map(lambda x: x[0], points)),list(map(lambda x: x[1], points)) )
plt.plot( list(map(lambda x: x[0], upperBound[1])), list(map(lambda x: x[1], upperBound[1])))
plt.title("Shortest Path: "+str(upperBound[0]))
plt.axis('square')
plt.show()

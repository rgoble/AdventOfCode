from collections import defaultdict
from heapq import heappop, heappush
from functools import cache
# with open("input.txt", "rt") as inp:
with open("sample.txt", "rt") as inp:    
    data =  inp.read().strip()

grid = {}
numRows = 0
numCols = 0 
for r,row in enumerate(data.split('\n')):
    numRows = max(numRows, r+1)
    for c,col in enumerate(row):
        numCols = max(numCols, c+1)
        grid[(r,c)] = col

# Find the starting point
start = None
for pt, val in grid.items():
    if val == 'S':
        start = pt
        break

if start is None:
    print("Error: Couldn't find starting point in the grid!")
    exit()

# directions
# 0 = n, 1 = w, 2 = s, 3 = e
DR = [-1,0,1,0]
DC = [0,-1,0,1]

# Compute the move cost to each part of the grid based on the starting point
@cache
def dijkstra(ptStart):

    visited = {}
    maxDist = 0
    Q = [(0,ptStart)]
    while Q:
        # Pop the current distance and point from the heap
        dist, currPt = heappop(Q)

        if currPt in visited:
            # Its already cached so skip it
            continue

        # Cache the point here so we don't have to check it again
        visited[currPt] = dist

        maxDist = max(maxDist, dist)

        for d in range(4):
            # Move in all 4 directions
            rr = currPt[0]+DR[d]
            cc = currPt[1]+DC[d]
            nextPt = (rr,cc)
            if nextPt in grid and grid[nextPt] != '#':
                # Make sure the new point is still inside the grid
                # and its not a rock.                
                 heappush(Q, (dist+1, nextPt))
    
    # Check the edges to find the spot with the shortest distance
    # this will be used as the starting point to the next copy of the grid
    best = [(maxDist, None) for i in range(4)]
    
    # num Rows and Colums are the same, but if not
    # the points outside of the grid won't be visited
    # anyway so it won't hurt anything    
    for x in range(max(numCols,numRows)):
        edges = [(0,x), (x,0), (numRows - 1, x), (x,numCols - 1)]
        for d in range(4):
            pt = edges[d]
            if pt in visited and visited[pt] < best[d][0]:
                # Shorter distance
                best[d] = (visited[pt], pt)

    # # Processed the whole grid so see how many spots could be reached


    return visited, best, maxDist

def getPossibleSpots(visited, maxSteps):
    oddEven = maxSteps % 2                
    ans = 0
    for pt, d in visited.items():
        if d <= maxSteps and (d % 2) == oddEven:
            ans += 1

    return ans

def buildGrid(visited, maxSteps):
    gridStr = []
    oddEven = maxSteps % 2                
    for r in range(numRows):
        row = []
        for c in range(numCols):
            pt = (r,c)
            if pt in visited and visited[pt] <= maxSteps and visited[pt] % 2 == oddEven:
                row.append('O')
            else:
                row.append(grid[pt])
        
        gridStr.append(''.join(row))

    return gridStr
    
def pt2(ptStart, maxSteps):
    ans = 0
    gridVisited = {}
    ptGrid = (0,0) # This is an index into the infinite grid copies
    tmpRowSet = set()
    tmpColSet = set()

    Q = [(0,ptGrid,ptStart)]
    while Q:
        # Pop the current distance and point from the heap
        dist, ptGrid,ptCurr = heappop(Q)

        if ptGrid in gridVisited:
            # Already calculated for this grid so skip it
            continue

        # Visit all of the points in the grid
        visited, best, maxDist = dijkstra(ptCurr)

        tmpRowSet.add(ptGrid[0])
        tmpColSet.add(ptGrid[1])

        # Cache that we have processed this grid copy
        gridVisited[ptGrid] = (dist,visited) #(dist, ptCurr)

        # Add up the number of spots in this grid copy
        # TODO: Optimize to not have to call this every time
        # if we know we are including all of the spots in a grid
        gridCnt = getPossibleSpots(visited, maxSteps - dist)
        ans += gridCnt
        print("Grid(%s) has %d spots, total = %d" % (list(ptGrid), gridCnt, ans))

        for d in range(4):
            # If best edge point in this direction is less than
            # or max step count
            newDist = dist + best[d][0] + 1
            if newDist < maxSteps:
                gr = ptGrid[0]+DR[d]
                gc = ptGrid[1]+DC[d]
                nextGrid = (gr,gc)

                sr = (best[d][1][0]+DR[d]) % numRows
                sc = (best[d][1][1]+DC[d]) % numCols
                nextPt = (sr,sc)

                heappush(Q, (newDist, nextGrid, nextPt))
    
    # Temp: Visualize the grid
    gridVis = {}
    print("Grid Vis Pt2: NumSteps = %d" % maxSteps)
    for gr in sorted(tmpRowSet):
        
        subGrids = defaultdict(list)
        for gc in sorted(tmpColSet):
            d = maxSteps
            visited = set()

            if (gr,gc) in gridVisited:
                d, visited = gridVisited[(gr,gc)]

            for rNum, rowStr in enumerate(buildGrid(visited, maxSteps - d)):
                subGrids[rNum].append(rowStr)            
        
        # Now print out the rows of grids on 1 lines        
        lineLen = 0
        for r in range(numRows):
            print(' | '.join(subGrids[r]))            

        # Now print out seperate between rows
        lineLen = len(' | '.join(subGrids[0]))            
        # print(' '*lineLen)
        print('-'*lineLen)
        # print(' '*lineLen)

    # gridStr = []
    # oddEven = maxSteps % 2                
    # for r in range(numRows):
    #     row = []
    #     for c in range(numCols):
    #         pt = (r,c)
    #         if pt in visited and visited[pt] % 2 == oddEven:
    #             row.append('O')
    #         else:
    #             row.append(grid[pt])
        
    #     gridStr.append(''.join(row))

    return ans

print('='*8)
visit, best,maxDist = dijkstra(start)
ans1 = getPossibleSpots(visit, 64)
print("Part1: %d" % ans1)

tests = [6,10,50,100,500,1000,5000]
tPass = [16,50,1594,6536,167004,668697,16733044]
for i,t in enumerate(tests):
    ans = pt2(start, t)
    result = 'Passed!'
    if ans != tPass[i]:
        result = 'Failed! (%d)' % tPass[i]
    print("Test #%2d: %d steps = %d %s" % (i,t,ans,result))
    if ans != tPass[i]:
        break


# # Create a new starting point 1 north
# newStart = ((shortP[0]+DR[0])%numRows, shortP[1]+DC[0])
# newDist = maxSteps - shortD - 1
# numN, visitedN = dijkstra(newStart, newDist)
# showGrid(visitedN, newDist)
# showGrid(visited,maxSteps)
# # print("Part1: %d" % dijkstra(start,7))
# print("Part1: %d" % dijkstra(start,8))
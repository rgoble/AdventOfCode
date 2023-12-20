from collections import defaultdict
from heapq import heappop, heappush


with open("input.txt", "rt") as inp:
# with open("sample.txt", "rt") as inp:    
    data =  inp.read().strip()

grid = [[int(c) for c in row] for row in data.split('\n')]

# directions
# 0 = n, 1 = w, 2 = s, 3 = e
DR = [-1,0,1,0]
DC = [0,-1,0,1]
OppDir = [2,3,0,1,5] # 5 is a special case for the 1st cell

numRows = len(grid)
numCol = len(grid[0])
bestLoss = 0xffffffffffff

def dijkstra(minRun, maxRun):
    # Starting point (row,col,dir,runLen)
    ptStart = (0,0,4,1)

    lossCache = {}
    Q = [(0,ptStart)]
    while Q:
        # Pop the current loss and point from the heap
        loss, currPt = heappop(Q)

        if currPt in lossCache:
            # Its already cached so skip it
            continue

        # Cache the loss to here so we don't have to do it again alter
        lossCache[currPt] = loss

        for d in range(4):
            # Make sure it's not opposite direction
            if d != OppDir[currPt[2]]:
                # Make sure we can move that way
                rr = currPt[0]+DR[d]
                cc = currPt[1]+DC[d]
                if 0 <= rr < numRows and 0 <= cc < numCol:                    
                    newLoss = loss + grid[rr][cc]
                    newLen = currPt[3]+1                    
                    if currPt[2] != 4 and d != currPt[2]:                        
                        # Tryin to change direction
                        if currPt[3] < minRun:
                            # Prev run didn't meet the min length, so can't turn yet
                            continue

                        # Change direction
                        newLen = 1

                    if newLen <= maxRun:
                        # print("\tMoving %d => (%d,%d) newLen = %d" % (d, rr, cc, newLen))       
                        heappush(Q, (newLoss, (rr,cc,d,newLen)))
    
    # Processed the whole grid so find the best value for 
    ans = float("inf")
    for (r,c,dir,runLen), loss in lossCache.items():
        if r == numRows - 1 and c == numCol - 1 and runLen >= minRun:
            ans = min(ans, loss)

    return ans

print('='*8)
print("Part1: %d" % dijkstra(1,3))
print("Part1: %d" % dijkstra(4,10))
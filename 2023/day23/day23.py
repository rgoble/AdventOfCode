
# 0 = U, 1 = L, 2 = D, 3 = R
DR = [-1,0,1,0]
DC = [0,-1,0,1]
steep = ['^','<','v','>']
noSteep = ['v','>','^','<']
grid = {}
numRow = 0
numCol = 0
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for r,line in enumerate(inp):        
        numRow = max(numRow, r)
        for c,path in enumerate(line):
            numCol = max(numCol, c)
            grid[(r,c)] = path


def showPath(grid,visited):
    for r in range(numRow):
        rowData = []
        pathData = []
        for c in range(numCol):
            pt = (r,c)
            rowData.append(grid[pt])

            if pt in visited:
                pathData.append('O')
            else:
                pathData.append(grid[pt])
        
        print('%s => %s' % (''.join(rowData), ''.join(pathData)))

def findLongest(grid, visited, currPt, endPt, dist):
    # Make a copy of the visited set
    myVisit = set(visited)
    myVisit.add(currPt)

    # If we reached the end point we are done
    if currPt == endPt:
        # if dist == 154:
        #     showPath(grid,visited)
        return dist
    
    longest = 0
    if grid[currPt] in steep:
        # Its a slope so we can only go 1 direction
        d = steep.index(grid[currPt])
        newPt = (currPt[0] + DR[d], currPt[1] + DC[d])
        if newPt in grid and grid[newPt] not in ['#', noSteep[d]] and newPt not in myVisit:
            longest = findLongest(grid, myVisit, newPt, endPt, dist+1)
    else:
        for d in range(4):
            newPt = (currPt[0] + DR[d], currPt[1] + DC[d])
            if newPt in grid and grid[newPt] not in ['#', noSteep[d]] and newPt not in myVisit:
                # Haven't went there yet so try going there
                longest = max(longest, findLongest(grid, myVisit, newPt, endPt, dist+1))

    return longest

ans1 = ans2 = 0

start = (0,1)
end = (numRow - 1, numCol - 2)
visited = set()
ans1 = findLongest(grid, visited, start,end, 1)

print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)        
from functools import cache

grid = []
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line = line.strip()
        if len(line) > 0:
            grid.append(list(line))

numRows = len(grid)
numCols = len(grid[0])

# might want to cache
@cache
def roll(path):        
    numRocks = path.count('O')
    numEmpty = len(path) - numRocks
    # print("\tRoll(%s) ==> '%s'" % (path, ''.join(['O'*numRocks, '.'*numEmpty])))
    return ''.join(['O'*numRocks, '.'*numEmpty])

@cache
def rollRocks(data):
    return '#'.join([roll(g) for g in data.split('#')])

def getLoad(grid):    
    load = 0
    numRows = len(grid)
    for r in range(numRows):
        load += (numRows - r) * grid[r].count('O')
    
    return load

# Run the spin cycle
i = 0
myCache = {}
ans = 0
while i < 1000000000:    

    # First lets see if this grid is already cached
    gridKey = '\n'.join(''.join(r) for r in grid)
    if myCache.get(gridKey) is not None:
        # Its cached
        print("Iter: %6d => First cached at %d, (Cycle = %d) Load = %d" %(i, myCache[gridKey], (i-myCache[gridKey]), getLoad(grid)))
        cycle = i - myCache[gridKey]
        i += ((1000000000 - i) // cycle) * cycle
    
    myCache[gridKey] = i

    # First tilt north
    for c in range(numCols):
        newC = rollRocks(''.join([r[c] for r in grid]))
        # Update the grid
        for r,val in enumerate(newC):
            grid[r][c] = val
    
    if ans == 0:
        # Solve part 1
        ans = getLoad(grid)

    # Tilt west
    for r in range(numRows):
        newR = rollRocks(''.join(grid[r]))
        # update grid
        grid[r] = list(newR)

    # Tilt south
    for c in range(numCols):
        # Grab the column and flip it, so it will roll in the opposite direction
        # be sure to flip it back after rolling
        newC = rollRocks(''.join([r[c] for r in grid])[::-1])[::-1]
        # Update the grid
        for r,val in enumerate(newC):
            grid[r][c] = val

    # Tilt east
    for r in range(numRows):
        # Grab the row, flip it so it will roll south
        newR = rollRocks(''.join(grid[r])[::-1])[::-1]
        # update grid
        grid[r] = list(newR)

    i = i + 1

print('='*8)
print("Part1: %d" % ans)
print("Part2: %d" % getLoad(grid))

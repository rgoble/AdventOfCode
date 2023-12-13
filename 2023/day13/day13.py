# from itertools import pairwise

def isHorzMirror(a,b,grid):
    if a < 0 or b >= len(grid):
        # Once either bound is outside the grid return true
        return True
    else:
        # Both are in bounds so see if they are the same
        if grid[a] == grid[b]:
            return isHorzMirror(a-1, b+1, grid)
        else:
            # They are different
            return False

def isVertMirror(a,b,grid):
    if a < 0 or b >= len(grid[0]):
        # Either side is out of bounds
        return True
    else:
        # Both are inbounds so see if they are the same
        # print("isVert(%d,%d) grid(%dx%d)" % (a,b,len(grid), len(grid[0])))
        aCol = [grid[r][a] for r in range(len(grid))]
        bCol = [grid[r][b] for r in range(len(grid))]
        if aCol == bCol:
            return isVertMirror(a-1, b+1, grid)
        else:
            # They are different
            return False

def getMirrorValue(grid):
    # Check rows first
    val = 0
    for r in range(len(grid)-1):
        # Loop over rows and look for 2 secutive rows thats are the the same
        if grid[r] == grid[r+1]:
            # Found a match, so check if the rest of the rows mirror
            if isHorzMirror(r, r+1, grid):
                # It's a Horizontal mirror so return num cols left of the mirror point
                val += 100*(r + 1)

    # Now check vertically
    for c in range(len(grid[0])-1):
        if [grid[r][c] for r in range(len(grid))] == [grid[r][c+1] for r in range(len(grid))]:
            # Found matching columns so check for vert mirror
            if isVertMirror(c, c+1, grid):
                val += (c+1)
    
    # Didn't find mirror point
    if val == 0: print("Didn't find mirror value")
    return val
        
ans = 0
grid = []

# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line = line.strip()
        if line != '':
            # Append it onto the current grid
            grid.append(line.strip())
        else:
            # This is the end of a grid so find the mirror point
            # print("=== Checking Mirror ===")
            # for r in grid:
            #     print(r)

            val = getMirrorValue(grid)
            ans += val
            print("=== Mirror: %d Total: %d ===" % (val, ans))
            # restart the grid
            grid = []

print("Part1 is not 33778")
print("Part1 is not 18059")
print('='*8)
print(ans)
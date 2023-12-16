# Note: I had to add an extra newline to the end of the input file, otherwise
# my code wouldn't process the last mirror so the results would be wrong

def isHorzMirror(a,b,grid, useSmudge):
    # print("\t\t\tisHorzMirror(%d,%d,...,useSmudge=%s)" % (a,b,useSmudge))
    if a < 0 or b >= len(grid):
        # Once either bound is outside the grid return true
        return True, useSmudge
    else:
        # Both are in bounds so see if they are the same
        diff = 0
        for col in range(len(grid[a])):
            if grid[a][col] != grid[b][col]:
                diff += 1

        if diff == 0:
            return isHorzMirror(a-1, b+1, grid, useSmudge)
        elif diff == 1 and useSmudge:
            # Smudge is available so use it
            return isHorzMirror(a-1, b+1, grid, False)
        else:
            # They are different
            return False, useSmudge

def isVertMirror(a,b,grid, useSmudge):
    if a < 0 or b >= len(grid[0]):
        # Either side is out of bounds
        return True, useSmudge
    else:
        # Both are inbounds so see if they are the same
        # print("isVert(%d,%d) grid(%dx%d)" % (a,b,len(grid), len(grid[0])))
        diff = 0
        for r in range(len(grid)):
            if grid[r][a] != grid[r][b]:
                diff += 1

        if diff == 0:
            return isVertMirror(a-1, b+1, grid, useSmudge)
        elif diff == 1 and useSmudge:
            # Smudge is avail so use it
            return isVertMirror(a-1, b+1, grid, False)
        else:
            # They are different
            return False, useSmudge

def getMirrorValue(grid, useSmudge):
    # Check rows first
    print("getMirrorValue(useSmudge=%s)" % useSmudge)
    val = 0    
    for r in range(len(grid)-1):
        # See if this is the middle of a mirror
        found, used = isHorzMirror(r, r+1, grid, useSmudge)

        if found and (useSmudge == False or used == False):
            # It's a Horizontal mirror so return num cols left of the mirror point
            val += 100*(r + 1)

        # print("\tRow: %2d | %s | %2d => val = %d (found=%s,used=%s)" % (r+1, grid[r], r+1, val, found, used))

    # Now check vertically
    for c in range(len(grid[0])-1):
        # exact match
        found, used = isVertMirror(c, c+1, grid, useSmudge)
        
        if found and (useSmudge == False or used == False):
                val += (c+1)
    
    # Didn't find mirror point
    if val == 0: print("Didn't find mirror value")
    return val
        
ans = 0
ans2 = 0
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

            val = getMirrorValue(grid, False)
            val2 = getMirrorValue(grid, True)
            ans += val
            ans2 += val2
            print("=== Mirror: %d (Smudge %d) Total: %d (%d)===" % (val, val2, ans, ans2))
            # restart the grid
            grid = []

print('='*8)
print("Part1: %d" % ans)
print("Part2: %d" % ans2)
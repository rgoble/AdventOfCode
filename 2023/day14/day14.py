
grid = []
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line = line.strip()
        if len(line) > 0:
            grid.append(list(line))

numRows = len(grid)
numCols = len(grid[0])

print("=== Before shift ===")
for r in grid:
    print(''.join(r))

# Tilt the rocks north

for c in range(numCols):
    # Skip the 1st row because it can't go anywhere
    moved = True
    while moved:
        moved = False
        for r in range(1,numRows):
            if grid[r][c] == 'O':
                # Its a round rock so try and move it north
                if grid[r-1][c] == '.':
                    # Its safe to move it
                    grid[r-1][c] = 'O'
                    grid[r][c] = '.'
                    moved = True

print("=== After shift ===")
for r in grid:
    print(''.join(r))

# Find load
ans = 0
for r in range(numRows):    
    rowLoad = (numRows - r) * grid[r].count('O')
    ans += rowLoad

print('='*8)
print("Part1: %d" % ans)


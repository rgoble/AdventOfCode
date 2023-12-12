from itertools import combinations

# Load the grid
grid = []
with open("input.txt", "rt") as inp:
    for line in inp:
        grid.append(line.strip())


# Look for empty rows and colums
dblRow = {}
galaxy = []
for row, line in enumerate(grid):
    empty = True
    for col,c in enumerate(line):
        if c == '#':
            # Its not empty
            empty = False
            # Save the galaxy position
            galaxy.append((row,col))

    if empty == True:
        dblRow[row] = True

# Look for empty cols
dblCol = {}
for col in range(len(grid[0])):
    empty = True
    for row in grid:
        if row[col] == '#':
            empty = False
            break
    
    if empty == True:
        dblCol[col] = True


# Loop over all of the combinations of galaxys
total = 0
total2 = 0
for g1,g2 in combinations(galaxy, 2):
    dRow = abs(g1[0] - g2[0]) # row difference
    dCol = abs(g1[1] - g2[1]) # col diff
    dist2 = dist = dRow + dCol
    for r in range(dRow):
        if dblRow.get(min(g1[0], g2[0])+r) is not None:
            # Needs double
            dist += 1
            dist2 += 999999                     
    for c in range(dCol):
        if dblCol.get(min(g1[1], g2[1])+c) is not None:
            # Double it
            dist += 1
            dist2 += 999999                     

    total += dist
    total2 += dist2

    # print("%s => %s distance: %d" % (g1,g2,dist))

print("="*8)
print("Total: %d" % total)
print("Total2: %d" % total2)
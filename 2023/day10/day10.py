pipeTypes = {
    '|': {'n':True, 'e': False, 's':True, 'w': False},
    '-': {'n':False, 'e': True, 's':False, 'w': True},
    'L': {'n':True, 'e': True, 's':False, 'w': False},
    'J': {'n':True, 'e': False, 's':False, 'w': True},
    '7': {'n':False, 'e': False, 's':True, 'w': True},
    'F': {'n':False, 'e': True, 's':True, 'w': False},
    'S': {'n':True, 'e': True, 's':True, 'w': True},
}

dirs = ['n','s','e','w']
grid = []
row = 0
sRow = -1
sCol = -1
with open("input.txt", "rt") as inp:
    for line in inp:        
        grid.append(line)
        if sCol == -1:
            sCol = line.find('S')
            if sCol != -1:
                sRow = row
        
        row += 1

lenY = len(grid)
lenX = len(grid[0])
dist = {}
currDist = 0
found = False
answer = -1
pos = [{'x':sCol,'y':sRow,'prev':' '}] # x, y, prevDir
while found == False:
    newPositions = []
    currDist += 1
    # print("Round #%05d numPts=%d" % (currDist,len(pos)))
    if len(pos) > 2: 
        break
    for p in pos:
        currPipe = grid[p['y']][p['x']]
        # print("\tPos: %s => currPipe: %s" % (p, currPipe))
        for d in dirs:
            if d != p['prev'] and pipeTypes[currPipe][d] == True:
                # its not where we came from, and this pipe supports going in that direction
                newP = {'x':p['x'],'y':p['y'],'prev':p['prev']}
                if d == 'n' and p['y'] - 1 >= 0:
                    newP['y'] -= 1
                    newP['prev'] = 's'                    
                elif d == 's' and p['y'] + 1 < len(grid):
                    newP['y'] += 1
                    newP['prev'] = 'n'                    
                elif d == 'w' and p['x'] -1 >= 0:
                    newP['x'] -= 1
                    newP['prev'] = 'e'
                elif d =='e' and p['x'] + 1 < len(grid[0]):
                    newP['x'] += 1
                    newP['prev'] = 'w'
                else:
                    print("Can't move from (%d,%d,%s)" % (p['x'], p['y'], currPipe))
                    continue

                # Make sure that pipe will accept connections from our direction
                newPipe = grid[newP['y']][newP['x']]                
                if pipeTypes[newPipe][newP['prev']] == True:                
                    # print("\t\tGoing %s (%s)" % (d, newP))
                    newPositions.append(newP)
                    key = '%d:%d' % (newP['x'], newP['y'])
                    if dist.get(key) is None:
                        # Save the distance
                        dist[key] = currDist
                    else:
                        # At the loop so we are done                        
                        answer = dist[key]
                        print("Max distance: %d" % answer)
                        found = True
                        break
                        
    # USe the new positiosn
    # print("NewPos = %s" % newPositions)
    pos = newPositions

def isInside(x, y, show=False):
    global grid, lenX, lenY, dist

    hits = {'w': 0, 'e': 0}    
    d = 'w'
    str = ''
    for xx in range(lenX):
        c = '.'        
        if xx == x:
            onLine = False
            d = 'e'
            c = '*'
        elif dist.get('%d:%d' % (xx,y)) is not None:
            # See if its a cross or on a line            
            p = grid[y][xx]
            if p in ['|', 'F', '7']: # count things that have a piece below the line
                hits[d]+= 1
                c = 'H'

        str += c
    
    if show == True:
        print(str)

    # Make sure its surrounded by the loop
    if min(hits.values()) > 0:
        if hits['w'] % 2 == 1 and hits['e'] % 2 == 1:
            return True
    
    return False

# Now loop over the grid and see if any points are inside,
# by casting "rays" in each direction to the edges. If all
# of the rays cross an odd number of pipe segments then
# the point is inside the loop
numInside = 0
newGrid = []
for y in range(lenY):
    newRow = ''
    for x in range(lenX):        
        # Make sure its not in the grid
        key = '%d:%d' % (x,y)
        if dist.get(key) is None:
            # This is not part of the loop so test it
            # Check west to east first
            inside = isInside(x,y,False)
            if inside == True:
                newRow += 'I'
                numInside += 1
            else:
                newRow += 'O'
        else:
            # Part of the loop
            newRow += grid[y][x]
    
    newGrid.append(newRow)


for r in newGrid:
    print(r)

print('')
print("Max Distance = %d" % answer)
print("NumInside = %d" % numInside)

                    
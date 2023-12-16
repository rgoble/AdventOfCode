from functools import cache
from collections import defaultdict

reflectors = {  '.': {'r':['r'], 'l':['l'], 'u':['u'], 'd':['d']},
                '/': {'r':['u'], 'l':['d'], 'u':['r'], 'd':['l']},
                '\\': {'r':['d'], 'l':['u'], 'u':['l'], 'd':['r']},
                '|': {'r':['u','d'], 'l':['u','d'], 'u':['u'], 'd':['d']},
                '-': {'r':['r'], 'l':['l'], 'u':['l', 'r'], 'd':['l','r']}
            }
data = []

# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    data =  inp.read().strip().split('\n')

R = len(data)
C = len(data[0])

# Beam is tuple (x, y, direction)
def moveBeam(beam, newDir):    
    x = beam[0]
    y = beam[1]
    if newDir == 'r':
        x += 1
    elif newDir == 'l':
        x -= 1
    elif newDir == 'u':
        y -= 1
    else:
        y += 1
    
    if (0 <= x < C) and (0 <= y < R):
        # print("\t\tmoveBeam(%s, %s) => (%d, %d, %s)" % (beam, newDir,x,y,newDir))
        return (x,y,newDir)
    
    # print("\t\tmoveBeam(%s, %s) => None" % (beam, newDir))
    return None

def getEnergized(beams):
    energized = defaultdict(int)
    traversed = {}

    while len(beams) > 0:        
        newBeams = []
        for b in beams:
            # Infinite loops are possible so make sure the beam
            # hasn't moved through this grid in this direction
            # before
            # print(type(b))
            # print("\tb = (%d,%d,%s)" % (b[0],b[1],b[2]))
            if traversed.get(b) is None:
                traversed[b] = True

                # Make the cell is energized
                energized[(b[0],b[1])] += 1

                # Find the new direction
                # print("Check grid @ %s" % b)
                gridCell = data[b[1]][b[0]]
                newDir = reflectors[gridCell][b[2]]
                # print('\t\tGridCell = %s, newDir = %s' % (gridCell, newDir))
                
                # Move the beam in the new directions
                for d in newDir:
                    newB = moveBeam(b, d)
                    if newB is not None:
                        newBeams.append(newB)
        
        # Update to the new beam set
        beams = newBeams

    return len(energized.items())

ans1 = getEnergized([(0,0,'r')])
ans2 = 0
for y in range(R):    
    ans2 = max(ans2, getEnergized([(0,y,'r')]), getEnergized([(C-1,y,'l')]))
    print("Y %d/%d  => ans2 = %d" % (y,R,ans2))
for x in range(C):
    ans2 = max(ans2, getEnergized([(x, 0, 'd')]), getEnergized([(x,R-1,'u')]))
    print("X %d/%d  => ans2 = %d" % (x,C,ans2))

# Show the grid
for i,r in enumerate(data):
    print("#%32d => %s" % (i,r))

print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)
        
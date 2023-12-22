from collections import defaultdict
from operator import itemgetter

# directions
# 0 = U, 1 = L, 2 = D, 3 = R
dirType = {'U':0, 'D':2, 'L':1, 'R':3}
DR = [-1,0,1,0]
DC = [0,-1,0,1]

minRng = [0,0]
maxRng = [0,0]
# key = startRow, value = [(col,startRow, stopRow)]
# vertLines = defaultdict(list)
vertLines = []
# key = row, value = [(startCol, stopCol)]
horzLines = defaultdict(list)
ans1 = 0
currPt = (0,0)  # row,col
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line=line.strip()
        if line != '':
            dChar,dist,rgb = line.split(' ')
            dist = int(dist)
            # print("line %s ==> Dir: %s, Dist =%d, rgb = %s" % (line, dChar, dist, rgb))
            # Lookup the direction type
            d = dirType[dChar]
            # calculate the new point
            newPt = (currPt[0] + dist*DR[d], currPt[1] + dist*DC[d])
            # Add the number of moves to the volume
            ans1 += dist

            # print("currPt %s => %s for %s" % (currPt, newPt, line))
            # Save the verticle lines, so they can be used later to 
            # calculate the volume
            if dChar in ['U', 'D']:
                # If a line going down (col, startRow, stopRow)
                vLine = (currPt[1], min(currPt[0], newPt[0]), max(currPt[0], newPt[0]))
                # vertLines[vLine[1]].append(vLine)
                vertLines.append(vLine)
                # print("\tvLine ", vLine)
            else:
                # Horizontal line, need to save it too
                horzLines[newPt[0]].append((min(currPt[1], newPt[1]), max(currPt[1], newPt[1])))

            # Update the min/max values for the row/columns
            for x in range(2):
                minRng[x] = min(minRng[x], newPt[x])
                maxRng[x] = max(maxRng[x], newPt[x])
            
            # Update currPoint
            currPt = newPt

gridFile = open('grid.txt','wt')
fillFile = open('gridFilled.txt','wt')

prem = ans1
print('Permiter = %d minRng=%s maxRng = %s' % (ans1,minRng, maxRng))
# Now that the grid is loaded, compute the area inside of the trench
currRow = minRng[0]
while currRow <= maxRng[0]:    
    # Get all of the lines that cross this row
    numDupRows = maxRng[0]
    vCross = []

    for vLine in vertLines: #.values():
        # col, startrow, stopRow
        if vLine[1] <= currRow < vLine[2]:
            # started at or above currRow, and ends after it, so
            # its a cross so save the line
            vCross.append(vLine)
            # Max # of duplicate rows is bottom of the shortest vert line
            numDupRows = min(numDupRows, (vLine[2] - currRow))
        elif vLine[1] > currRow:
            # It starts after the currRow, so the numDuplicates
            # can't be great than it
            # print('Had to cut a dup row run short')
            numDupRows = min(numDupRows, (vLine[1] - currRow))

    # Need to sort vCrosses by the column number
    vCross = sorted(vCross, key=itemgetter(0))

    # Save maxPossDups
    possDups = maxPossDups = numDupRows
    # Temp disable dup rows
    numDupRows = 1

    # print("currRow = %d, numDups = %d, vCross = %s" % (currRow, numDupRows, vCross))
    # print("\tHorzLines = %s" % horzLines[currRow])
    # print("currRow: %d, totalBefore = %d (maxDups = %d)" % (currRow, ans1, numDupRows))
    ansB4 = ans1

    # Temp code to draw the grid
    rowStr = list('.' * (maxRng[1] - minRng[1]+1))
    for vLine in vertLines:
        if vLine[1] <= currRow:
            if currRow < vLine[2]:
                # It crosses here
                rowStr[vLine[0]+abs(minRng[1])] = '#'
    
    # Now fill in any horz lines
    for hLine in horzLines[currRow]:
        for c in range(hLine[0], hLine[1]+1):
            rowStr[c+abs(minRng[1])] = '#'
    
    gridFile.write('%4d: %s\n' % (currRow, ''.join(rowStr)))
    # print("%3d: %s" % (r+currRow, ''.join(rowStr)))



    # Loop over the vert crossings
    totalOverlap = 0
    for i in range(len(vCross)-1):
        # If its inside
        if i % 2 == 0:
            # print("\t%s => %s is Inside" % (vCross[i], vCross[i+1]))
            # Make sure its not part of a horiztonal line (startCol, stopCol)
            # print("checking horz lines for ", vCross[i])
            isHorzLine = False
            
            for hLine in horzLines[currRow]:                
                if hLine[0] == vCross[i][0] and hLine[1] == vCross[i+1][0]:
                    # This horz line connects our 2 vert lines and it was already counted
                    # print('\t\t\tSkipping horz line ', hLine)
                    isHorzLine = True
                    # Since a least 1 part of this row has a horz line, we can only 
                    # safely count 1 row
                    numDupRows = 1
                    possDups = 1
                elif hLine[0] == vCross[i][0] or hLine[1] == vCross[i+1][0]:
                    # This horz line either starts with our left vert line, or
                    # it ends with our right vert lines. So we will need to remove
                    # the overlaps so they don't get counted twice
                    numOvelap = hLine[1] - hLine[0]
                    totalOverlap += numOvelap
                    
                    # print("\t\t\tHorz line %s overlaps, removing %d duplicates" % (hLine, numOvelap))
                    ans1 = ans1 - numOvelap                    

            if not isHorzLine:
                # Its not part of a line so add it to the volume
                numInside = (vCross[i+1][0] - vCross[i][0]) - 1
                for x in range(numInside):
                    col = (vCross[i][0] + abs(minRng[1])) + x + 1
                    rowStr[col] = 'I'                

                ans1 += (numDupRows * numInside)
                # ans1 += numInside
                # print("\t\tFound %d inside (Duplicate for %d rows), newTotal = %d" % (numInside, numDupRows, ans1))

    fillFile.write('%4d: %s - Inside %d, Overlap %d\n' % (currRow, ''.join(rowStr), (ans1 - ansB4), totalOverlap))
    # print("currRow %d, total = %d" % (currRow, ans1))
    print("\tFound %d inside, newTotal = %d (possDups %d)" % (ans1 - ansB4, ans1, numDupRows))
    numDupRows = 1
    if len(vCross) > 0:
        # Skip duplicate rows
        currRow += numDupRows
    else:
        # only jump 1 row
        currRow += 1

gridFile.close()
fillFile.close()

ans2 = 0
print('='*8)
print("Part1 49564 is too high")
print("Part1 49558 is wrong")
print("Part1 48795 is correct")
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)        
from collections import defaultdict
from operator import itemgetter

# directions
# 0 = U, 1 = L, 2 = D, 3 = R
dirType = {'U':0, 'D':2, 'L':1, 'R':3}
part2DirChar = ['R','D','L','U']
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
            
            # Part2                
            # print(rgb)
            dist = int(rgb[2:7], 16)
            dChar = part2DirChar[int(rgb[7])]
            d = dirType[dChar]            
            # print("line %s ==> Dir: %s, Dist =%d, rgb = %s" % (line, dChar, dist, rgb))
            # Lookup the direction type
            
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

# gridFile = open('grid.txt','wt')
# fillFile = open('gridFilled.txt','wt')

prem = ans1
print('Permiter = %d minRng=%s maxRng = %s' % (ans1,minRng, maxRng))
# Now that the grid is loaded, compute the area inside of the trench
currRow = minRng[0]
rowArea = totalArea = 0
prevHasCorners = True
while currRow <= maxRng[0]:    
    if not prevHasCorners and len(horzLines[currRow]) == 0:
        # If the last line didn't have horz lines, and this one
        # doesn't either, then the area must be the same
        totalArea += rowArea
        currRow += 1
        continue

    # Get all of the lines that cross this row
    vCross = []
    for vLine in vertLines: #.values():
        # col, startrow, stopRow
        if vLine[1] <= currRow < vLine[2]:
            # started at or above currRow, and ends after it, so
            # its a cross so save the line
            vCross.append(vLine)

    # Need to sort vCrosses by the column number
    vCross = sorted(vCross, key=itemgetter(0))

    rowArea = 0
    prevHasCorners = False

    # # Temp code to draw the grid
    # rowStr = list('.' * (maxRng[1] - minRng[1]+1))
    # for vLine in vertLines:
    #     if vLine[1] <= currRow:
    #         if currRow < vLine[2]:
    #             # It crosses here
    #             rowStr[vLine[0]+abs(minRng[1])] = '#'
    
    # # Now fill in any horz lines
    # for hLine in horzLines[currRow]:
    #     for c in range(hLine[0], hLine[1]+1):
    #         rowStr[c+abs(minRng[1])] = '#'
    
    # gridFile.write('%4d: %s\n' % (currRow, ''.join(rowStr)))

    # Loop over the vert crossings
    hLinesUsed = []
    prevHasCorners = False
    for i in range(len(vCross)-1):
        # If its inside
        if i % 2 == 0:                                    
            for hLine in horzLines[currRow]:        
                prevHasCorners = True     
                if hLine[0] == vCross[i][0] and hLine[1] == vCross[i+1][0]:
                    # This is the top of an upside down U, It will get counted
                    # as inside of the polygon, so no need to count it now
                    # if currRow == -116:
                    #     print("\tvInside %d - case 1 skipping hline %s" % (i, hLine))
                    hLinesUsed.append(hLine)
                elif hLine[0] == vCross[i][0] or hLine[1] == vCross[i+1][0]:
                    # This horz line either starts with our left vert line, or
                    # it ends with our right vert lines. It will get counted as inside
                    # so we don't need to count it now
                    # if currRow == -116:
                    #     print("\tvInside %d - case 2 skipping hline %s" % (i, hLine))                    
                    hLinesUsed.append(hLine)
                elif hLine[1] == vCross[i][0] or hLine[0] == vCross[i+1][0]:
                    # This horz line ends with our left edge, or starts with the right one
                    # so it will be outside of the polygon, so we will need to add it
                    # so it gets counted
                    if hLine not in hLinesUsed:
                        # if currRow == -116:
                        #     print("\tvInside %d - case 3 1st time adding %d for hline %s" % (i, (hLine[1]-hLine[0]),hLine))                        
                        # Make sure we didn't already count it
                        rowArea += (hLine[1] - hLine[0])
                        hLinesUsed.append(hLine)
                    else:
                        # if currRow == -116:
                        #     print("\tvInside %d - case 3 2nd time (sub 1) for hline %s" % (i, hLine))                        
                        rowArea -= 1

                    #     # This line connects to two edges, so need to +1 to 
                    #     # handle when we see it a 2nd time
                    #     rowArea += 1                        
                elif vCross[i][0] < hLine[0] and hLine[1] < vCross[i+1][0]:
                    # if currRow == -116:
                    #     print("\tvInside %d - case 4 for hline %s" % (i, hLine))                        

                    # Horiz line is the bottom of a U, and its completly within the inside
                    # area so it will already be counted
                    hLinesUsed.append(hLine)
            
            # count up the area inside the two edges
            numInside = (vCross[i+1][0] - vCross[i][0]) + 1
            # if currRow == -116:
            #     print("\t\t%d added" % numInside)
            rowArea += numInside
            # for x in range(numInside):
            #     col = (vCross[i][0] + abs(minRng[1])) + x
            #     rowStr[col] = '#'                
            
    # The only horzLines that won't get processed in the code above is for lines that
    # form the bottom of a U shape. This appens because the verticle lines on either
    # side of it will be both be considered "above" the current row, so they won't be
    # counted as intersections for the inside/outside test. So we will need to add them
    # now so they are counted towards the area
    notUsed = []
    for hLine in horzLines[currRow]:
        if hLine not in hLinesUsed:
            notUsed.append(hLine)
            rowArea += hLine[1] - hLine[0] + 1

    totalArea += rowArea

    # fillFile.write('%4d: %s - RowArea: %d, Total: %d\n' % (currRow, ''.join(rowStr), rowArea, totalArea))
    # if len(notUsed) > 0:
    #     print("currRow %d, rowArea: %d, Total = %d, NotUsed: %s" % (currRow, rowArea, totalArea, notUsed))
    currRow += 1

ans1 = totalArea
# gridFile.close()
# fillFile.close()

ans2 = 0
print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)        
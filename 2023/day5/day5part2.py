# Load the input

def parseSeeds(str):
    # First strip of the seeds part to leave just the numbers
    str = str[7:]

    # Split on space to seperate out the numbers
    seeds = []
    for s in str.split(' '):
        if s != '':     # Ignore blanks due to double spaces
            seeds.append(int(s))

    return seeds            

class MapRange:
    def __init__(self, mapStr) -> None:
        # Parse the values from the string
        vals = mapStr.split(' ')

        self.destStart = int(vals[0])
        self.srcStart = int(vals[1])
        self.size = int(vals[2])

    def lookUp(self, srcVal):
        # Calculate different between requested value, and the
        # starting source value for this range
        srcDelta = srcVal - self.srcStart
        if 0 <= srcDelta < self.size:
            # Calculate remaing number of items in this range
            rangeLeft = self.size - srcDelta
            # if rangeLeft == 0:
            #     print("\tZero left in lookup src %d in Range(%s)" %(srcVal, self) )
            #     print("\t\tsrcDelta = %d, left = %d" % (srcDelta, rangeLeft))
            # If the srcDelta is within our range then return the dest val
            return self.destStart + srcDelta, rangeLeft

        # Not within our range so return None
        return None, None

    def __str__(self) -> str:
        return "dest: %12d, src: %12d, size: %d" % (self.destStart, self.srcStart, self.size)
            

class Map:
    def __init__(self, name) -> None:
        self.name = name
        self.ranges = []

    def lookUp(self, srcVal):
        highRanges = []
        for r in self.ranges:
            val, left = r.lookUp(srcVal)
            if val is not None:
                # We found the value in a range, so return it
                # print("\tMap: %s Range(%s) - Lookup %d Output %d Left %d" % (self.name, r, srcVal, val, left))
                return val, left
            elif r.srcStart > srcVal:
                # Our value isn't in this range, but this range is higher than our value
                # so we will add it to the list of higher ranges. We will use this list
                # if our number isn't within any range to see how much room is left after
                # it until the next range starts
                highRanges.append(r.srcStart)

        # By default, if its not in any of the ranges of the map 
        # then the value doesn't change, but we need to figure out 
        # how much room is left before the next range starts
        left = 0xffffffff
        if len(highRanges) > 0:            
            left = min(highRanges)
            # print("\tIn %s, left %12d, HighRanges: %s" % (self.name, left, highRanges))
        # else:
        #     print("\tIn %s, nothing Higher than\n\t\t             %12d" % (self.name, srcVal))
        #     for r in self.ranges:
        #         print("\t\tRange: %s" % r)

        # print("Not in a range (Left = %d)!" % left)
        return srcVal, left

seeds = []
mapName = ''
maps = {}

# Parese the input
with open("input.txt", "rt") as inp:
    for line in inp:
        if line.startswith('seeds:'):
            # Line contains the seeds
            seeds = parseSeeds(line)
            print(seeds)
        elif line.find('map') != -1:
            # Start of a new map
            mapName, extra = line.split(' ')
            maps[mapName] = Map(mapName)
        elif line != '\n':
            # Its part of a range
            maps[mapName].ranges.append(MapRange(line))

# Try and find the lowest location for the seeds
lowestLoc = None
cnt = 0
# Treat Seeds a ranges
for i in range(0, len(seeds), 2):
    print("#%04d: start=%d size=%d" % (i, seeds[i], seeds[i+1]))
    s = seeds[i]
    seedEnd = seeds[i]+seeds[i+1]
    while s < seedEnd:
        # First covnert seedNum to soilNum
        soil, left1 = maps['seed-to-soil'].lookUp(s)
        fert, left2 = maps['soil-to-fertilizer'].lookUp(soil)
        wat, left3 = maps['fertilizer-to-water'].lookUp(fert)
        lite, left4 = maps['water-to-light'].lookUp(wat)
        temp, left5 = maps['light-to-temperature'].lookUp(lite)
        hum, left6 = maps['temperature-to-humidity'].lookUp(temp)
        loc, left7 = maps['humidity-to-location'].lookUp(hum)        

        if lowestLoc is None:
            lowestLoc = loc
        else:
            lowestLoc = min(lowestLoc, loc)
        
        # print("\tVals = Seed: %11d Soil: %11d Fert: %11d Water: %11d Lite: %11d Temp: %11d Hum: %11d Loc: %11d Lowest: %11d" % (s, soil, fert, wat, lite, temp, hum, loc, lowestLoc))
        # print("\tSeed: %12d, Location %12d, Lowest: %12d" % (s, val, lowestLoc))        
        # A lot of the look ups cover a range, so get the numLeft from each lookup range used
        # for this seed. Take the min of that, and we can skip over that many seeds because
        # the locations will only increase
        skip = max(1, min(left1,left2, left3, left4, left5, left6,left7)) # Skip over at least 1        
        # print("\tLeft = Seed: %11d Soil: %11d Fert: %11d Water: %11d Lite: %11d Temp: %11d Hum: %11d Loc: %11d Skip: %11d" % (s, left1, left2, left3, left4, left5, left6, left7, skip))
        s += skip
        # print("\tSkipping: %d" % skip)

        cnt += 1


print("Lowest: %d" % lowestLoc)


        
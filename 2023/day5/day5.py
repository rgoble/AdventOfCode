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
        if 0 <= srcDelta <= self.size:
            # If the srcDelta is within our range then return the dest val
            return self.destStart + srcDelta

        # Not within our range so return None
        return None
            

class Map:
    def __init__(self, name) -> None:
        self.name = name
        self.ranges = []

    def lookUp(self, srcVal):
        for r in self.ranges:
            val = r.lookUp(srcVal)
            if val is not None:
                # We found the value in a range, so return it
                return val

        # By default, if its not in any of the ranges of the map 
        # then the value doesn't change
        return srcVal

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
for s in seeds:
    # First covnert seedNum to soilNum
    val = maps['seed-to-soil'].lookUp(s)
    val = maps['soil-to-fertilizer'].lookUp(val)
    val = maps['fertilizer-to-water'].lookUp(val)
    val = maps['water-to-light'].lookUp(val)
    val = maps['light-to-temperature'].lookUp(val)
    val = maps['temperature-to-humidity'].lookUp(val)
    val = maps['humidity-to-location'].lookUp(val)

    if lowestLoc is None:
        lowestLoc = val
    else:
        lowestLoc = min(lowestLoc, val)
    
    print("Seed: %12d, Location %12d, Lowest: %12d" % (s, val, lowestLoc))



        
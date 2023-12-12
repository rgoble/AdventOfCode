class Cubes:
    def __init__(self) -> None:
        self.red = 0
        self.green = 0
        self.blue = 0        
    
    def parse(self, roundStr):
        # Split the round by commas so each number / color pair are split
        cubes = roundStr.split(',')
        for x in cubes:
            # print("\t\t\tCubes: '%s'" % x.strip())
            numStr, color = x.strip().split(' ')
            num = int(numStr)
            if color == 'red':
                self.red = num
            elif color == 'green':
                self.green = num
            elif color == 'blue':
                self.blue = num
            else:
                print('Unknown color %s' % color)                

class Game:
    def __init__(self) -> None:
        self.id = 0
        self.rounds = []
    
    def parse(self, gameStr):
        # Split on the : to split the rounds and the game header
        gameInfo, roundInfo = gameStr.split(":")
        # print("GameStr: %s" % gameStr)
        # print("\tGameInfo: %s" % gameInfo)
        # print("\tRoundInfo: %s" % roundInfo)

        # Now pull out the game number
        self.id = int(gameInfo[5:])

        # Now split the rounds
        rounds = roundInfo.split(';')
        for rStr in rounds:
            # print("\t\tRound: %s" % rStr)
            r = Cubes()
            r.parse(rStr)
            self.rounds.append(r)
    
    def getMax(self):
        # Loop over the rounds and count the max of each cube color
        maxCubes = Cubes()
        for r in self.rounds:
            maxCubes.red = max(maxCubes.red, r.red)
            maxCubes.green = max(maxCubes.green, r.green)
            maxCubes.blue = max(maxCubes.blue, r.blue)

        return maxCubes

# Load the file of games and loop over them to look for ones
# that would be possible with 12 red, 13 green, and 14 blue cubes. 
# Then add up their game ID's
sum = 0
with open("input.txt", "rt") as inp:
    for line in inp:
        g = Game()
        g.parse(line)
        
        maxC = g.getMax()
        sum += (maxC.red * maxC.green * maxC.blue)
        # if maxC.red <= 12 and maxC.green <= 13 and maxC.blue <= 14:
        #     print("Sum: %6d => %s" % (sum, line))
        #     sum += g.id

print("="*8)
print(sum)
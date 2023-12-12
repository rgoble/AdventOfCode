class Card:
    def __init__(self, str) -> None:        
        # First split out the card number
        cardInfo, numberInfo = str.split(':')

        # Extract the card number
        self.id = cardInfo[5:]

        # Now slipt the numbers into the winning and ones on the card
        winningStr, yourNums = numberInfo.split('|')

        self.winners = self.parseNumbers(winningStr)
        self.nums = self.parseNumbers(yourNums)

    def parseNumbers(self, numStr):
        numList = numStr.strip().split(' ')        
        result = []
        for x in numList:
            if x != '':
                result.append(int(x))
        
        return result
    
    def getPoints(self):
        pts = 0
        for x in self.winners:
            if x in self.nums:
                # We have this number
                if pts == 0:
                    pts = 1
                else:
                    pts = pts * 2

        return pts

# Load the cards
sum = 0
with open("input.txt", "rt") as inp:
    for line in inp:
        c = Card(line)
        sum += c.getPoints()

        print("Sum: %6d - Points %4d - Card: %s" % (sum, c.getPoints(), line[:-1]))

print("="*8)
print(sum)
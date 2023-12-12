class Card:
    def __init__(self, str) -> None:        
        # First split out the card number
        cardInfo, numberInfo = str.split(':')

        # Extract the card number
        self.id = cardInfo[5:]
        self.numCopies = 1

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

    def getMatches(self):
        matches = 0
        for x in self.winners:
            if x in self.nums:
                # We have this number
                matches += 1

        return matches

# Load the cards
cards = []
with open("input.txt", "rt") as inp:
    for line in inp:
        cards.append(Card(line))

# Find the # of copies we win of each card
numCards = len(cards)
sum = 0
for i in range(numCards):
    c = cards[i]
    numMatch = c.getMatches()

    print("Card %s: %8d Copies, %2d matches" % (c.id, c.numCopies, numMatch))
    # Loop over numMatches and add up the copies
    for j in range(numMatch):
        idx = i + j + 1
        if idx < numCards:
            cards[idx].numCopies += c.numCopies

    # Count up the total after copies
    sum += c.numCopies

print("="*8)
print(sum)
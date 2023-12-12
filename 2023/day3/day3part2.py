class Part:
    def __init__(self, numStr, idxStart, idxEnd) -> None:
        self.num = int(numStr)
        self.idxStart = idxStart
        self.idxEnd = idxEnd

    def isAdjacent(self, idx):
        return (self.idxStart-1) <= idx <= (self.idxEnd+1)

class Symbol:
    def __init__(self, symbol, idx) -> None:
        self.symbol = symbol
        self.idx = idx

class Row:
    def __init__(self) -> None:
        self.Parts = []
        self.Symbols = []

    def getPartSum(self, idx):
        sum = 0
        for p in self.Parts:
            if p.isAdjacent(idx):
                sum += p.num

        return sum

    def getAdjacentParts(self, idx, parts):
        for p in self.Parts:
            if p.isAdjacent(idx):
                parts.append(p.num)


digits = ['0','1','2','3','4','5','6','7','8','9']
engine = []
# Load the engine schematic
with open("input.txt", "rt") as inp:    
    for line in inp:
        numStr = ''
        startIdx = -1
        currRow = Row()
        for i in range(len(line)):
            if line[i] in digits:
                # It's a digit so see if we need to start a new part number or 
                # if we are continuing
                if startIdx == -1:
                    # Start of a new number
                    startIdx = i
            else:
                # Not a digit, so see if we need to end a part number
                if startIdx != -1:
                    # We were in a number so we found the end of it
                    currRow.Parts.append(Part(line[startIdx:i], startIdx, i-1))
                    startIdx = -1
                
                if line[i] != '.' and line[i] != '\n':
                    # Its a symbol so add it
                    currRow.Symbols.append(Symbol(line[i], i))
        
        # Add this row to the schematic
        engine.append(currRow)

# Now that the schematic is loaded its time to find part numbers
sum = 0
numRows = len(engine)
for r in range(numRows):
    # Loop over the symbols in the current row
    row = engine[r]    
    for s in row.Symbols:
        # Look for gear symboles '*'
        if s.symbol == '*':
            parts = []

            # Get adjacent part numbers in the prev row
            if r > 0:
                engine[r-1].getAdjacentParts(s.idx, parts)
        
            # Get adjacent part numbers in curr
            row.getAdjacentParts(s.idx, parts)

            # Next row
            if r < (numRows - 1):
                engine[r+1].getAdjacentParts(s.idx, parts)
            
            if len(parts) == 2:
                print("Found a gear! %d * %d" % (parts[0], parts[1]))
                sum += (parts[0] * parts[1])
        
print("="*8)
print(sum)
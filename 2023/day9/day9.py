class Seq:
    def __init__(self) -> None:
        self.vals = []
    
    def parse(self, str):
        self.vals = []
        for s in str.split(' '):
            self.vals.append(int(s))

    def allZeros(self):
        for x in self.vals:
            if x != 0:
                return False
        
        return True
        
    def getDiffs(self):
        diffSeq = Seq()
        for i in range(1, len(self.vals)):
            diff = self.vals[i] - self.vals[i-1]
            diffSeq.vals.append(diff)

        return diffSeq
    
    def getNextVal(self) -> int:
        if self.allZeros():
            return 0
        else:
            return self.vals[-1] + self.getDiffs().getNextVal()

    def getPrevVal(self) -> int:
        if self.allZeros():
            return 0
        else:
            return self.vals[0] - self.getDiffs().getPrevVal()
    
    
allSeqs = []
with open("input.txt", "rt") as inp:
    for line in inp:
        seq = Seq()
        seq.parse(line)
        allSeqs.append(seq)

# Loop over all of the sequences
sum = 0
sumPrev = 0
for s in allSeqs:
    next = s.getNextVal()
    prev = s.getPrevVal()
    sum += next
    sumPrev += prev
    print("NextSum %d => PrevSum %d" % (sum, sumPrev))

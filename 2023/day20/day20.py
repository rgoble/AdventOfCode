from collections import defaultdict,deque
from math import gcd

class FlipFlop:
    def __init__(self, name) -> None:
        # 0 = Off, 1 = On
        self.name = name
        self.currState = 0
        self.inputs = []
        self.dest = []

    def pulse(self, fromName:str, pulse:int):
        nextPulse = []
        if pulse == 0: # Low Pulse
            self.currState = (self.currState + 1) % 2

            for mName in self.dest: 
                nextPulse.append((self.name, mName, self.currState))
        
        return nextPulse

    def __repr__(self) -> str:
        return '%d' % self.currState

class Conjunction:
    def __init__(self, name) -> None:
        self.name = name
        self.lastPulse = defaultdict(int)
        self.inputs = []
        self.dest = []
    
    def pulse(self, fromName:str, pulse:int):
        # Save new pulse state
        self.lastPulse[fromName] = pulse
                
        sendPulse = 0
        for inp in self.inputs:
            if self.lastPulse[inp] == 0:
                sendPulse = 1
                break
        
        nextPulse = []
        for mName in self.dest: 
            nextPulse.append((self.name, mName, sendPulse))
        
        return nextPulse

    def __repr__(self) -> str:        
        return '{%s}' % (','.join(['%s=%d' % (k,self.lastPulse[k]) for k in self.inputs]))
        

class Broadcast:
    def __init__(self) -> None:
        self.name = 'broadcaster'
        self.inputs = []
        self.dest = []
    
    def pulse(self, fromName:str, pulse:int):
        nextPulse = []
        for mName in self.dest: 
            nextPulse.append((self.name, mName, pulse))
        
        return nextPulse

    def __repr__(self) -> str:
        return self.name

def lcm(cycleCnts):
    fact = 1
    for c in cycleCnts:
        fact = (c*fact)//gcd(c, fact)
    
    return fact

M = {}
# with open("sample2.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line=line.strip()
        if line != '':
            name, outs = line.split('->')
            m = None
            if name.startswith('broadcaster'):
                m = Broadcast()
            elif name[0] == '%':
                m = FlipFlop(name[1:].strip())            
            elif name[0] == '&':
                m = Conjunction(name[1:].strip())
            else:
                print('Unexpected line! %s' % line)
                continue

            # Setup the outputs
            m.dest = [x.strip() for x in outs.split(',')]

            # Add module to the dict
            M[m.name] = m

# Need to init all of the modules inputs
for inpName,inp in M.items():
    for out in inp.dest:
        if out in M:
            M[out].inputs.append(inpName)

ans1 = 0
ans2 = 0
pCnt = [0,0] # low,High
lowCache = {}
cycles = {}
# pt2Nodes = ['mq','tz','xf','tg']
pt2Nodes = ['lh','fk','ff','mm']
pulses = deque()
i = 0
inProgress = True
while inProgress:

    # pulse is a tuple(src,dest,signal)
    pulses.append(('button','broadcaster',0))

    while pulses:
        src,dest,p = pulses.popleft()

        # Update pulse count
        pCnt[p] += 1

        # Cache low pulses
        if p == 0:
            if dest in pt2Nodes and dest in lowCache:
                # We can compute the cycle for this node
                cycles[dest] = i - lowCache[dest]
                print("%6d: Found cycle for %s => %s" % (i,dest,cycles))

            # Cache low pulses
            lowCache[dest] = i
        
            if len(cycles.keys()) == len(pt2Nodes):
                # We have seen the cycle for all of the nodes
                # so calculate # of presses
                ans2 = lcm(cycles.values())
                inProgress = False
                break

        # Grab module
        if dest in M:
            m = M[dest]
            # Pulse
            newPulses = m.pulse(src, p)
            for nextP in newPulses:
                pulses.append(nextP)

    # Increment the button counter
    i += 1
    if i == 1000:
        ans1 = pCnt[0]*pCnt[1]

print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)        
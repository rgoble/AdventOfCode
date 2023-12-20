from collections import defaultdict

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

def pushButton(currMods, debug=False):
    # low, high
    pulseCount = [0,0]
    rxLow = False
    # pulse is a tuple(src,dest,signal)
    pulses = [('button','broadcaster',0)]

    while len(pulses) > 0:
        # make list of next set of pulses
        if debug: print('== Phase (numPulses = %d) ==' % len(pulses))
        newPulses = []
        for src,dest,p in pulses:
            if debug: print('\t%s - %d => %s' % (src,p,dest))

            # Pt2
            if p == 0 and dest == 'rx':
                rxLow = True

            # Update pulse count
            pulseCount[p] += 1
            # Grab module
            if dest in currMods:
                m = currMods[dest]
                # Pulse
                newPulses += m.pulse(src, p)
            # else:
            #     print("Warning: module %s doesn't exist" % dest)
        
        # update pulses to the new list
        pulses = newPulses

    return pulseCount, rxLow

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

def modState(M):
    key = sorted(M.keys())
    return ','.join(['%s=%s' % (k,M[k]) for k in key])

# Need to init all of the modules inputs
for inpName,inp in M.items():
    for out in inp.dest:
        if out in M:
            M[out].inputs.append(inpName)

i = 0
pushLimit = 1000
pCnt = [0,0] # low,High
initModState = modState(M)
rxTrigger = pushLimit

print("initState: %s" % initModState)
while i < pushLimit:
    newCnt,rxLow = pushButton(M)
    i += 1

    if rxLow:
        rxTrigger = min(rxTrigger, i)

    # Count up the number of new pulses
    for p in range(2):
        pCnt[p] += newCnt[p]
    
    newState = modState(M)
    # print("%4d: %s newCnt:%s tot:%s" % (i, newState, newCnt, pCnt))
    if newState == initModState:
        print("Found initial state after %d presses" % i)
        # Completed a full cycle of the modules
        # So we can just skip processing the other presses
        numCycles = (pushLimit - i) // i
        print('numCycles = %d' % numCycles)
        # multiple the number of pulses by num of cycles we are skipping
        for p in range(2):
            pCnt[p] += (pCnt[p]*numCycles)
        
        # Update the current press count to match what we skipped
        i += (numCycles * i)
        

# key = sorted(M.keys())
# print("Module state: {%s}" % ','.join(['%s=%s' % (k,M[k]) for k in key]))
# print("\tCycles: %s" % pushButton(M))
# print("Module state: {%s}" % ','.join(['%s=%s' % (k,M[k]) for k in key]))
# print("\tCycles: %s" % pushButton(M))
# print("Module state: {%s}" % ','.join(['%s=%s' % (k,M[k]) for k in key]))
# print("\tCycles: %s" % pushButton(M))
# print("Module state: {%s}" % ','.join(['%s=%s' % (k,M[k]) for k in key]))
# print("\tCycles: %s" % pushButton(M))
# print("Module state: {%s}" % ','.join(['%s=%s' % (k,M[k]) for k in key]))

ans1 = pCnt[0]*pCnt[1]
ans2 = rxTrigger
print('='*8)
print("Part1: Low=%d,High=%d Total=%d" % (pCnt[0],pCnt[1],ans1))
print("Part2: %d" % ans2)        
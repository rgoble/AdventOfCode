from collections import defaultdict
from heapq import heappop, heappush
from copy import deepcopy

workflow = {}
parts = []
isWorkFlow = True
# with open("sample.txt", "rt") as inp:    
with open("input.txt", "rt") as inp:
    for line in inp:
        line=line.strip()
        if line == '':
            isWorkFlow = False
        elif isWorkFlow:
            idx = line.find('{')
            name = line[:idx]
            rules = line[idx+1:-1].split(',')
            workflow[name] = rules
        else:
            idx = line.find('{')
            d = {}
            for vals in line[idx+1:-1].split(','):
                k,v = vals.split('=')
                d[k] = int(v)

            parts.append(d)

def getValue(part, wf):
    # print('getValue(%s, %s)' % (part,wf))
    if wf == 'A':
        t = sum(part.values())
        # print('Found total: %d for part %s' % (t, part))
        return t
    elif wf == 'R':
        # print("Rejected: %s" % part)
        return 0
    
    for r in workflow[wf]:
        # print('\tRule: %s' % r)
        if ':' in r:
            # Its a compairson
            cond, next = r.split(':')
            var = cond[0]
            op = cond[1]
            val = int(cond[2:])

            if op == '<':
                if part[var] < val:
                    return getValue(part, next)
            elif op == '>':
                if part[var] > val:
                    return getValue(part,next)
            else:
                print("Unexpected op %s" % op)
                return 0
        else:
            # Default so follow it
            return getValue(part, r)
    
    # Shouldn't get here but just in casse
    print("Erorr hit unexpected end")
    return 0

def getPossible(wf, minRng, maxRng, dept=0):
    # print("%sgetPossible(%s, min:%s, max:%s)" % ('\t'*dept, wf, minRng, maxRng))
    if wf == 'A':
        t = 1
        # Calculate number of combinations
        for v in minRng.keys():
            t *= ((maxRng[v] - minRng[v])+1)
        # print("%s\tAccept: %d" % ('\t'*dept, t))
        return t
    elif wf == 'R':
        # print("%s\tReject: 0" % ('\t'*dept))
        return 0

    # Return early of the ranges every get crossed
    for k,v in minRng.items():
        if v > maxRng[k]:
            # Min > Max
            print("%s\tMin/Max crossed for %s => Min: %s Max: %s" % ('\t'*dept, k, minRng, maxRng))
            return 0
    
    # Copy the ranges
    newMin = minRng.copy()
    newMax = maxRng.copy()
    t = 0
    for r in workflow[wf]:
        if ':' in r:
            # Its a compairson
            cond, next = r.split(':')
            var = cond[0]
            op = cond[1]
            val = int(cond[2:])

            if op == '<':
                # Its a new maximum value 
                tmpMax = newMax.copy()
                tmpMax[var] = min(val-1, tmpMax[var])
                t += getPossible(next, newMin, tmpMax, dept+1)
                # Now that we returned update our current limits
                # because it will affected the conditions after this one
                newMin[var] = max(val, newMin[var])
            elif op == '>':
                # Its a new min value
                tmpMin = newMin.copy()
                tmpMin[var] = max(val+1, tmpMin[var])
                t += getPossible(next, tmpMin, newMax, dept+1)
                # Update current limits
                newMax[var] = min(val, newMax[var])
        else:
            # Default so follow it
            t += getPossible(r, newMin, newMax, dept+1)
    
    return t

ans1 = 0
for p in parts:
    ans1 += getValue(p, 'in')

minRng = {}
maxRng = {}
for v in ['x','m','a','s']:
    minRng[v] = 1
    maxRng[v] = 4000

ans2 = getPossible('in', minRng, maxRng)    

print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)
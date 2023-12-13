from itertools import product

allFound = []
def getCombos(springs, data, currLen, s):
    global allFound
    # print("getCombos([%s],%s,%d) => '%s'" % (springs, data, currLen, s))
    # Check end conditions    
    if len(springs) == 0:        
        if len(data) == 0 and currLen == 0:
            # Exhausted both so its valid
            # print("\tFound #1 => '%s'" % s)
            allFound.append(s)
            return 1
        elif len(data) == 1 and currLen == data[0]:
            # matched the last data
            # print("\tFound #2 => '%s'" % s)
            allFound.append(s)
            return 1
        else:            
            # Out of springs but still have data left so this
            # isn't a valid option
            # print("\tInvalid #0 => '%s'" % s)
            return 0

    # its either a blank, or the end of a run of springs    
    if springs[0] == '.':
        s += '.'
        if currLen == 0:
            # This is a working spring, and not part of block
            # so just continue processing
            return getCombos(springs[1:], data, 0, s)
        elif len(data) > 0 and currLen == data[0]:
            # This is the end of a run bad springs and it matches
            # our required size so it's good so far. So just Keep
            # processing the rest of the strings and data
            return getCombos(springs[1:], data[1:], 0, s)
        else:
            # This is the end of a run and it didn't match
            # the needed size, so its a failed possibility
            # print("Data exhausted #1 => '%s'" % s)
            return 0
    elif springs[0] == '#':
        s += '#'
        # Increment the currLen
        currLen += 1
        if len(data) == 0:
            # data was already exhausted
            # print("Data exhausted #2 => '%s'" % s)
            return 0

        if currLen <= data[0]:
            # It could still be a valid solution so keep going
            return getCombos(springs[1:], data, currLen, s)
        else:
            # This pushes us over the max size for this block
            # so it's a failed combo
            # print("Block too large => '%s'" % s)
            return 0
    else:
        # Its unknown, so try it as both
        # print("\tUnknown len=%d data[0]=%d" % (currLen, data[0]))
        sum = 0

        if currLen == 0:
            # Not in a run so just continue as normal
            sum = getCombos(springs[1:], data, 0, s+'.')
        elif len(data) > 0 and currLen == data[0]:
            # If we were in the middle of a run and treat it as working
            # we can end the run and continue processing
            # print("\tTreating as good!")
            sum = getCombos(springs[1:], data[1:], 0, s+'.')
        elif len(data) > 0 and currLen > data[0]:
            # Its invalid
            # print("Invalid #1 => '%s'" % s)
            return 0
        
        # We also want to treat it as broken and count those possibilites        
        return sum + getCombos(springs[1:], data, currLen+1,s+'#')
    
ans = 0
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line = line.strip()
        springs, data = line.split(" ")
        
        springs = '?'.join(springs for x in range(5))
        data = ','.join(data for x in range(5))
        data = [int(x) for x in data.split(',')]
        # print("\tx5 springs = %s  ==> Data: %s" % (springs, data))

        # if line != "?###???????? 3,2,1":
        #     continue

        s = ''
        combos = getCombos(springs, data, 0, s)
        ans += combos
        print("%s ==> %d combos" % (line, combos))
        # for x in allFound:
        #     print("\t%s" % x)

print('='*8)
print(ans)

            


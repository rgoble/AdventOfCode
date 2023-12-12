from itertools import product

sum = 0
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line = line.strip()
        springs, data = line.split(" ")
        recs = [int(x) for x in data.split(',')]

        # Get number of unknowns
        numUnknown = springs.count('?')        

        print("%d Unknowns in Line: %s" % (numUnknown, line))
        # Loop over all of the combinations of possible solutions
        # . = operational, # = damaged, ? = unknown
        for cmb in product('#.', repeat=numUnknown):   
            # Replace each ? in the line with the combination
            tmp = line
            for x in cmb:
                tmp = tmp.replace('?', x, 1)

            # print("\tComb: %s ==> %s" % (cmb, tmp))                
            
            groups = []
            b = 0
            for x in tmp:
                if x == '#':
                    # Its broke so increment count
                    b += 1
                elif b > 0:
                    # Working spring after run of broken ones
                    groups.append(b)
                    b = 0
            
            if len(groups) == len(recs):
                # Same number of groups, so see if they have the same values
                match = True
                for i, num in enumerate(groups):
                    if num != recs[i]:
                        match = False
                        break
                
                if match == True:
                    sum += 1

print('='*8)
print(sum)

            


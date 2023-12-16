from functools import cache

# data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
with open("input.txt", "rt") as inp:
    data =  inp.read().strip()



def hash(str):
    h = 0
    for c in str:
        h =  ((h + ord(c)) * 17) % 256
    return h

ans = 0
box = [[] for x in range(256)]
for seq in data.split(','):
    # part1
    ans += hash(seq)

    # part2
    # break the sequence up into parts
    label = focal = None
    opInsert = False
    if seq[-1] == '-':        
        label = seq[:-1]
    else:
        opInsert = True
        label, focal = seq.split('=')
    
    h = hash(label)
    if opInsert:
        replaced = False
        for slot,lense in enumerate(box[h]):
            if label == lense[0]:
                # Matches label so replace it
                box[h][slot] = (label, int(focal))
                replaced = True
                break
        
        if not replaced:
            # Need to insert it
            box[h].append((label, int(focal)))

    else:
        for lense in box[h]:
            if label == lense[0]:
                # Matches label so remove it
                box[h].remove(lense)
                break

print("Boxes")
print('='*8)
ans2 = 0
for i,b in enumerate(box):    
    if len(b) > 0:
        for s,l in enumerate(b):
            ans2 += (i+1)*(s+1)*l[1]

        print("Box %3d: %s" % (i,b))

print('='*8)
print("Part1: %d" % ans)        
print("Part2: %d" % ans2)        
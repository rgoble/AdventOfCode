from collections import defaultdict

# directions
# 0 = U, 1 = L, 2 = D, 3 = R
dirType = {'U':0, 'D':2, 'L':1, 'R':3}
DR = [-1,0,1,0]
DC = [0,-1,0,1]

rowRng = [0,0]
colRng = [0,0]
# key = col, value = [(startRow, stopRow)]
vertLines = {}
volume = 0
currPt = (0,0)
# with open("sample.txt", "rt") as inp:
with open("input.txt", "rt") as inp:
    for line in inp:
        line=line.strip()


ans1 = 0
ans2 = 0
print('='*8)
print("Part1: %d" % ans1)
print("Part2: %d" % ans2)        
from math import gcd

#         Node: DXL Cycles: [12168, 24337, 36506, 48675, 60844, 73013]
#         Node: VRV Cycles: [20092, 40185, 60278, 80371]
#         Node: ZZZ Cycles: [20658, 41317, 61976, 82635]
#         Node: TMH Cycles: [22356, 44713, 67070]
#         Node: SFF Cycles: [13300, 26601, 39902, 53203, 66504, 79805]
#         Node: CKP Cycles: [18960, 37921, 56882, 75843]

# There has to be some way to "solve" for this to find the right factor
# 12169a = 20093b  => a = (20093b)/12169
# 20093b = 20659c  => b = (20659c)/20093
# 20659c = 22357d  => c = (22357d)/20659
# 22357d = 13301e  => d = (13301e)/22357
# 13301e = 18961f  => e = (18961f)/13301
# 18961f = 12169a  => f = (12169a)/18961
cycleCnt = [12169, 20093, 20659, 22357, 13301, 18961]

# The largest cycle will be our step size
stepSize = max(cycleCnt)
step = -1
cnt = 0
done = False

while done == False:
    cnt += 1
    step += stepSize
    matches = []
    numTrue = 0
    for i in range(len(cycleCnt)):
        if (step % cycleCnt[i]) == cycleCnt[i] - 1:
            # It would end in Z
            matches.append(True)
            numTrue += 1
        else:
            matches.append(False)
    
    if numTrue > 4:
        #57733437: Step=702558194852 Matches=[True, True, True, True, True, False]
        print("#%06d: Step=%12d Matches=%s" % (cnt, step, matches))

    if False not in matches:
        # Find them all
        done = True

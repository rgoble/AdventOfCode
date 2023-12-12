# Input values
time = [40828492]
dist = [233101111101487]

def getNumWaysToWing(time, winDist):
    numWins = 0
    for speed in range(1, time):
        timeLeft = time - speed
        d = speed * timeLeft
        if d > winDist:
            numWins += 1
            if numWins % 1000000 == 0:
                print("\tTime: %d, WinDist %d, (%d * %d) = %d, numWays= %8d" % (time, winDist, speed, timeLeft, d, numWins))
            

    return numWins

margin = 0
for r in range(len(time)):    
    wins = getNumWaysToWing(time[r], dist[r])
    print("Race #%d => %d ways to win" % (r, wins))
    margin = wins

print("="*8)
print("margin: %d" % margin)
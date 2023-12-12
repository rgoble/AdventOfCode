# Input values
time = [40,82,84,92]
dist = [233, 1011, 1110, 1487]

def getNumWaysToWing(time, winDist):
    win = []
    for speed in range(1, time):
        timeLeft = time - speed
        d = speed * timeLeft
        if d > winDist:
            print("\tTime: %d, WinDist %d, (%d * %d) = %d" % (time, winDist, speed, timeLeft, d))
            win.append([speed, d])

    return win

margin = 0
for r in range(len(time)):
    print("Race #%d" % r)
    wins = getNumWaysToWing(time[r], dist[r])
    if margin == 0:
        margin = len(wins)
    else:
        margin *= len(wins)

print("="*8)
print("margin: %d" % margin)
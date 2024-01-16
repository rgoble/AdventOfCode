
with open('gridFilled.txt', 'rt') as inp:
    for line in inp:
        rowNum = int(line[:4])
        data = line[6:511]
        kv = line[514:].split(', ')
        # print(kv)
        rArea = int(kv[0].split(': ')[1])
        total = int(kv[1].split(': ')[1])
        cnt = data.count('#')
        if cnt != rArea:
            print("for row %d, the area %d doesn't match count %d" % (rowNum, rArea, cnt))
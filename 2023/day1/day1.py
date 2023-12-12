#digits = ['0','1','2','3','4','5','6','7','8','9','zero','one','two','three','four','five','six','seven','eight','nine']
digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4,'5': 5,'6': 6, '7': 7, '8': 8, '9': 9,
          'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
sum = 0 
with open("input.txt", "rt") as inp:
    for line in inp:
        firstDigit = lastDigit = ''
        for x in range(len(line)):
            for d in digits.keys():
                # Check from the start
                if firstDigit == '' and line[x:x+len(d)] == d:
                    # Found it
                    firstDigit = d
                            
                # Check from the end
                if lastDigit == '':
                    rIdx = (len(line) - 1) - x 
                    if line[rIdx:rIdx+len(d)] == d:
                        lastDigit = d
            
            if firstDigit != '' and lastDigit != '':
                break;
        
        # Conver it to a number
        num = (10 * digits[firstDigit]) + digits[lastDigit]
        sum += num
        print('Digit: %02d Sum: %06d String: "%s"' % (num, sum, line))

print("="*8)
print(sum)
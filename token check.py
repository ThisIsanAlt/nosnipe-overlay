j = '100000000003227'

condition1 = False
condition2 = False
condition3 = False


if int(j[0]) + int(j[2]) + int(j[4]) + int(j[6]) + int(j[8]) + int(j[10]) + int(j[12]) % 9 == 0:
    condition1 = True
    print('condition1')
if int(j[1]) + int(j[3]) + int(j[5]) + int(j[7]) + int(j[9]) + int(j[11]) % 8 == 0:
    condition2 = True
    print('condition2')
if int(j[0]) + int(j[1]) == int(j[11]) + int(j[12]):
    condition3 = True
    print('condition3')
if condition1 and condition2 and condition3:
    print('FOUND:', j)
condition1 = False
condition2 = False
condition3 = False

for j in range(100000000000000, 999999999999999):
    j = str(j) 

    if int(j[0]) + int(j[2]) + int(j[4]) + int(j[6]) + int(j[8]) + int(j[10]) + int(j[12]) % 9 == 0:
        condition1 = True
    if int(j[1]) + int(j[3]) + int(j[5]) + int(j[7]) + int(j[9]) + int(j[11]) % 8 == 0:
        condition2 = True
    if int(j[0]) + int(j[1]) == int(j[11]) + int(j[12]):
        print(f'conidition3: ')
        condition3 = True

    if condition1 and condition2 and condition3:
        print(condition1 , condition2, condition3)
        print('FOUND:', j)
    
    if int(j) % 100000 == 0:
        print('HEARTBEAT:', j)

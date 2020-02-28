line = input('Please input the int sequences:')
lst = list(map(int, line.split(' ')))
new_lst = []
new_lst.append([lst[0], 1])
j = 0
for i in range(1, len(lst)):
    if lst[i] != lst[i-1]:
        j += 1
        new_lst.append([lst[i], 1])
    else:
        new_lst[j][1] += 1
for i in range(len(new_lst)):
    print(new_lst[i][1], new_lst[i][0], end=' ')
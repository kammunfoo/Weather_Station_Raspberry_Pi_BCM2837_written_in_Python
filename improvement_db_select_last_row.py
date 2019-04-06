list1 = ['a', 'b', 'c', 'd', 'e',]
for index, item in enumerate(list1):
    print(index, item)

print()
length = len(list1)
print(length - 1, list1[length - 1])

print()
print(list1[-1])

print()
list2 = ['abcde', 'bcdef', 'cdefg', 'defgh', 'efghi',]
length = len(list2[-1]) - 1
record = 'eeee ' + list2[-1][length - length] + '\n'
record += 'afff ' + list2[-1][length - length + 1] + '\n'
record += 'geee ' + list2[-1][length - length + 2] + '\n'
record += 'aage ' + list2[-1][length - length + 3] + '\n'
record += 'aiii ' + list2[-1][length - length + 4] + '\n'
print(record)

print()
for index, row in enumerate(list2[-1]):
    print(index, row)
    if index == 0:
        record = 'eeee ' + row + '\n'
    elif index == 1:
        record += 'afff ' + row + '\n'
    elif index == 2:
        record += 'geee ' + row + '\n'
    elif index == 3:
        record += 'aage ' + row + '\n'
    else:
        record += 'aiii ' + row + '\n'
print(record)
    

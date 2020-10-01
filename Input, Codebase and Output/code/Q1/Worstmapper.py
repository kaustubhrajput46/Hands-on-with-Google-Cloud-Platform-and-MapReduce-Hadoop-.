#!/usr/bin/env python
import sys
# input comes from STDIN (standard input)
list_iterator = iter(sys.stdin)
next(list_iterator)

# for max temp
max_temp = 0
nested_list = []
for line in list_iterator:

#for line in sys.stdin[1:]:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(",")
    for word in words:
        desired = int(words[2])
        actual = int(words[3])
        system = int(words[4])
        age = int(words[5])
        diff = abs(desired - actual)
        output = []
        output.insert(0, diff)
        output.insert(1, system)
        output.insert(2, age)
        # max difference
        if (diff > max_temp):
            max_temp = diff
    # add this output list in new list (Nested List)
    nested_list.append(output)

j = []
max_temp_list = []
sort_list = []
for i in nested_list:
    if(i[0] == max_temp):
        # add age and system ID in the list
        new_list = [];
        new_list.insert(0, i[2])
        new_list.insert(1, i[1])
        new_list.insert(2, i[0])
        sort_list.append(new_list)

sort_list.sort()
for j in sort_list:
    print(' '.join(map(str, j)))


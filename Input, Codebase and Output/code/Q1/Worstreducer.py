#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
worst_1 = 0
worst_2 = 0
worst_3 = 0
main_list = []
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    sub_list = []
    # parse the input we got from mapper.py
    system_age, system_id, temp_diff  = line.split(' ')
    sub_list.insert(0, int(system_age))
    sub_list.insert(1, int(system_id))
    sub_list.insert(2, int(temp_diff))

    main_list.append(sub_list)

main_list.sort()

Worst_systems = main_list[-3:]
worst_3 = Worst_systems[0]
worst_2 = Worst_systems[1]
worst_1 = Worst_systems[2]

print 'First worst system with id =', worst_1[1], 'and age =', worst_1[0], ' with temperature diff of ', worst_1[2]
print 'Second worst system with id =', worst_2[1], 'and age =', worst_2[0], ' with temperature diff of ', worst_1[2]
print 'Third worst system with id =', worst_3[1], 'and age =', worst_3[0], ' with temperature diff of ', worst_1[2]

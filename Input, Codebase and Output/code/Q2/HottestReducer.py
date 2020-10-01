#!/usr/bin/env python
from operator import itemgetter
import sys

main_list = []
# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    sub_list = []
    # parse the input we got from mapper.py
    time, temp, system, building = line.split(' ')
    sub_list.insert(2, building)
    sub_list.insert(0, time)
    sub_list.insert(1, temp)
    main_list.append(sub_list)


#new dict with time, building as the key
time_stamp_with_total_temp = {}
time_stamp_with_total_occurrence = {}
for listt in main_list:
    if (listt[0], listt[2]) in time_stamp_with_total_occurrence.keys():
        time_stamp_with_total_temp[(listt[0], listt[2])] = int(time_stamp_with_total_temp.get((listt[0], listt[2]))) + int(listt[1])
        time_stamp_with_total_occurrence[(listt[0], listt[2])] = int(time_stamp_with_total_occurrence.get((listt[0], listt[2]))) + 1
    else :
        time_stamp_with_total_temp[(listt[0], listt[2])] = int(listt[1])
        time_stamp_with_total_occurrence[(listt[0], listt[2])] = 1

llist = []
#print the total temp list
time_stamp_with_avg_temp = {}
for ((time_0, building_0), temp) in time_stamp_with_total_temp.items():
#    print(time_0, building_0, temp)
#    print(time_0, building_0, time_stamp_with_total_occurrence.get((time_0, building_0)))
    time_stamp_with_avg_temp[(time_0, building_0)] = int(temp) / time_stamp_with_total_occurrence.get((time_0, building_0))
#    llist.append([building_0, time_0, time_stamp_with_avg_temp[(time_0, building_0)]])

    print time_0,",", building_0,",", time_stamp_with_avg_temp[(time_0, building_0)]



#calculate average temp per time stamp
time_stamp_with_avg_temp = {}
for ((time, building), temp) in time_stamp_with_total_temp.items():
    time_stamp_with_avg_temp[(time, building)] = int(temp) / time_stamp_with_total_occurrence.get((time, building))


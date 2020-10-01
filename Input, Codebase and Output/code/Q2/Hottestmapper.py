#!/usr/bin/env python
import sys
import datetime 
import calendar 
#from datetime import datetime
#from datetimerange import DateTimeRange

# input comes from STDIN (standard input)
list_iterator = iter(sys.stdin)
next(list_iterator)


def time_in_range(x):
    start = datetime.datetime.strptime("08:00:00", '%H:%M:%S').time()
    end = datetime.datetime.strptime("16:00:00", '%H:%M:%S').time()
    """Return true if x is in the range [start, end]"""
    #print x
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

#find day for working hours
def findDay(date): 
    get_day  = datetime.datetime.strptime(date, '%m %d %Y').weekday() 
    day = str(calendar.day_name[get_day])
    #print (day)
    if day == "Sunday" or day == "Saturday" :
#        print(calendar.day_name[get_day])
        return ('not_working_day')
    else :
        return ('working_day')
spam =0;



# create an empty dict for building temp
#building temp ={"building_number": total_temperature}
building_temp = {}

# create an empty dict for number of systems in a building
#building temp ={"building_number": total building}
building_sys = {}

#maintain list for working days 
working_hour_list = []
for line in list_iterator:
    # remove leading and trailing whitespace
    line = line.strip()
    # split the line into words
    words = line.split(",")
    for word in words:
        date = words[0]

        date_list = date.split('/')
        day = findDay(' '.join(map(str, date_list)))#1

        #get time
        #get normal working hour time (8am -4am)
        #print time
        get_time = datetime.datetime.strptime(words[1], '%H:%M:%S').time()

        is_working_hour = time_in_range(get_time)#2

        actual = int(words[3])#3
        system = int(words[4])#4
        buildingId = int(words[6])#5
    if day == 'working_day' and str(is_working_hour) == "True":
        #create a sublist
        working_hour_sublist = []
        #time of the this tuple
        working_hour_sublist.insert(0, words[1])
        #Actual temp of this tuple
        working_hour_sublist.insert(1, actual)
        #System Id of this tuple
        working_hour_sublist.insert(2, system)
        #Building Id of this tuple
        working_hour_sublist.insert(3, buildingId)
        #Adding this list to working_hour_list
        working_hour_list.append(working_hour_sublist)

        #print "In the working hour range"
        spam += 1 #to check no of records
        if (buildingId, system) in building_temp.keys():
            #add temp to the total temp for this building
            building_temp[(buildingId, system)] = building_temp.get((buildingId, system)) + actual
            #increment the systems for this building
            building_sys[(buildingId, system)] = building_sys.get((buildingId, system)) + 1
        else :
            building_temp[(buildingId, system)] = actual
            building_sys[(buildingId, system)] = 1

building_sys_avg_temp = {}
#now get the avg of each sys for each bldg
for ((bldgId, sysId), number) in building_sys.items():
#    building_sys_avg_temp[(bldgId, sysId)] = building_temp.get((bldgId, sysId)) / building_sys.get((bldgId, isysId))
    building_sys_avg_temp[(bldgId, sysId)] = building_temp.get((bldgId, sysId)) / number
#    print (bldgId, sysId, ":", building_sys_avg_temp.get((bldgId, sysId)))
#building_sys_avg_temp


#new dictionary to store the average temperature.
building_total_temp = {1:0} 
building_sys_present = {}
#for ((bldgId, sysId), avg) in building_sys_avg_temp.items():
for ((bldgId, sysId), avg) in building_sys_avg_temp.items():
    #for each iteration, increment temp for that particular building
    if (bldgId, sysId) in building_total_temp.keys():
#        print ('---------')
#        print (bldgId, sysId, avg)
        building_total_temp[bldgId] = building_total_temp.get(bldgId) + avg
        building_sys_present[bldgId] = building_sys_present.get(bldgId) + 1
    else :
        building_total_temp[bldgId] = avg
        building_sys_present[bldgId] = 1

#need to calc avg temp for each building
building_avg_temp = {}
for (id, unique_system) in building_sys_present.items():
    building_avg_temp[id] = building_total_temp.get(id) / unique_system



#for (id, avg) in building_avg_temp.items():
#    print (id,":",avg)

#sort the dict based on avg temperatures.
import operator
sorted_d = sorted(building_avg_temp.items(), key=operator.itemgetter(1))

##print the sorted list
#for q in sorted_d:
#    print q

#get the greatest three elements of list(hottest buildings)
Hottest_buildings = sorted_d[-3:]

hot_blgs = []
#for i in range(0, len(Hottest_buildings)):
for (id, temp) in Hottest_buildings :
#   Hottest_buildings[i] = int(i[0])
#   print(Hottest_buildings[0])
    hot_blgs.append(id)
#    print(id)


#get all the tuples for these three buildings
for slist in working_hour_list:
    if int(slist[3]) in hot_blgs:
        print(' '.join(map(str, slist)))



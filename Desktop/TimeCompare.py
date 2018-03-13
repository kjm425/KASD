from datetime import datetime
from dateutil import tz
import re

schedule = open("myschedule.txt", 'r')

def ScheduleParse():
    with open("myschedule.txt", 'r') as file:
        filecontent= str(file.read())
        filecontent= filecontent.split(";")
        for element in range(len(filecontent)):
            filecontent[element] = filecontent[element].split("|")
            for classes in range(len(filecontent[element])):
                filecontent[element][classes]=filecontent[element][classes].split(",")
        return filecontent
zed = ScheduleParse()
def TimeCompare(day,classnum):
    timezone = tz.gettz("EST")
    tim = re.findall('\d+:\d\d\s\w\w',zed[day][classnum][1])[0]
    tim = tim.replace(":",'')
    print(tim)
    timnum = int(re.findall("\d+",tim)[0])
    if (tim[-2] == 'p') & (tim[0:2]!="12"):
        timnum += 1200
    curtime= int(str(datetime.now(tz=timezone).hour) + str(datetime.now(tz=timezone).minute))
    if curtime >= timnum:
        return True
    else:
        return False

print(TimeCompare(4,3))
schedule.close()
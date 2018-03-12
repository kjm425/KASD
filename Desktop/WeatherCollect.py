import requests
import serial
import datetime
import time
import math
from time import strftime, localtime
from dateutil import tz
import re

def ScheduleParse():
    with open("myschedule.txt", 'r') as file:
        filecontent= str(file.read())
        filecontent= filecontent.split(";")
        for element in range(len(filecontent)):
            filecontent[element] = filecontent[element].split("|")
            for classes in range(len(filecontent[element])):
                filecontent[element][classes]=filecontent[element][classes].split(",")
        return filecontent
def TimeCompare(day,classnum):
    timezone = tz.gettz("EST")
    tim = re.findall('\d+:\d\d\s\w\w',zed[day][classnum][1])[0]
    tim = tim.replace(":",'')

    timnum = int(re.findall("\d+",tim)[0])
    if tim[-2] == 'p':
        timnum += 1200
    curtime= int(str(datetime.datetime.now(tz=timezone).hour) + str(datetime.datetime.now(tz=timezone).minute))
    if curtime >= timnum:
        return True
    else:
        return False

apikey = "351315e12c05d02c854514b10129db23"
url = "https://api.darksky.net/forecast/"+apikey+"/39.958377,%20-75.189106"
apiinfo=requests.get(url).json()
temp= str(apiinfo['currently']['temperature'])

date=datetime.datetime.fromtimestamp((apiinfo['currently']['time']))
day=date.weekday()
days={0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
weekday=days[day]
schedule = open("myschedule.txt",'r')

#print("Weather conditions outside North Hall are "+str(apiinfo['currently']['summary']).lower()+".")
#conditions = "<" + "Conditions: "+str(apiinfo['currently']['summary']).lower() + ">"
date = "<" + (str(strftime("%Y-%m-%d %H:%M:%S", localtime())).center(20)) +">"
temperature = "<" + ("Temp:" +str(math.floor(float(temp)))+"F "+str(apiinfo['currently']['summary'][0]).upper()+str(apiinfo['currently']['summary'][1:]).lower()).center(20) + ">"
temperature = temperature.encode("utf-8")
date = date.encode("utf-8")
ser = serial.Serial(port="COM4",baudrate=9600)

zed=ScheduleParse()
waitfor = ''
while waitfor == "":
    time.sleep(0.1)
    waitfor = ser.read()
ser.flush()
#ser.write(date)
#ser.write(temperature)

#day is numerical day of week, may have to write an if statement to make sure it still works on weekends
lasttime=0
while True:
    apiinfo=requests.get(url).json()
    temp= str(apiinfo['currently']['temperature'])
    date = "<" + (str(strftime("%Y-%m-%d %H:%M:%S", localtime())).center(20)) + ">"
    curtime = datetime.datetime.timestamp(datetime.datetime.now())
    if (lasttime+240)<curtime:
        temperature = "<" + ( str(math.floor(float(temp))) + "F " + str(apiinfo['currently']['summary'][0]).upper() + str(apiinfo['currently']['summary'][1:]).lower()).center(20) + ">"
        temperature = temperature.encode("utf-8")
        lasttime = curtime
        print("weathertaken")
    date = date.encode("utf-8")
    ser.write(date)
    ser.write(temperature)
    #only displays future classes
    serobjs=[]
    for elements in range(1 ,len(zed[day])):
        if not TimeCompare(day,elements):
            clas = "<"+zed[day][elements][0][0:8].center(20)+">"
            tim = "<"+ zed[day][elements][1].center(20) + ">"
            bytelines=clas.encode("ascii")
            serobjs.append(bytelines)
            ser.write(bytelines)
            times = tim.encode("ascii")
            serobjs.append(bytelines)
    if serobjs !=[]:
        for stuff in range(0,len(serobjs)+1,2):
            ser.write(serobjs[stuff])
            ser.write(serobjs[stuff+1])
            time.sleep(5)
    else:
        donemessage= "<" +"No more classes.".center(20)+">"
        done= "<"+"Time to study.".center(20)+ ">"
        donemessage= donemessage.encode("ascii")
        done=done.encode("ascii")
        ser.write(donemessage)
        ser.write(done)

ser.close()

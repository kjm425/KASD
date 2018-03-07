import requests
import serial
import datetime
import time
import math
from time import strftime, localtime

def ScheduleParse():
    with open("myschedule.txt", 'r') as file:
        filecontent= str(file.read())
        filecontent= filecontent.split(";")
        for element in range(len(filecontent)):
            filecontent[element] = filecontent[element].split("|")
            for classes in range(len(filecontent[element])):
                filecontent[element][classes]=filecontent[element][classes].split(",")
        return filecontent

apikey="351315e12c05d02c854514b10129db23"
url="https://api.darksky.net/forecast/"+apikey+"/39.958377,%20-75.189106"
accountsid="AC7f79374c0d2133a1cdea9029f71856ac"
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
ser = serial.Serial(port="/dev/ttyACM1",baudrate=9600)

zed=ScheduleParse()
waitfor = ''
while waitfor == "":
    time.sleep(0.1)
    waitfor = ser.read()
ser.flush()
#ser.write(date)
#ser.write(temperature)

#day is numerical day of week, may have to write an if statement to make sure it still works on weekends
while True:
    apiinfo=requests.get(url).json()
    temp= str(apiinfo['currently']['temperature'])
    date = "<" + (str(strftime("%Y-%m-%d %H:%M:%S", localtime())).center(20)) + ">"
    temperature = "<" + ( str(math.floor(float(temp))) + "F " + str(apiinfo['currently']['summary'][0]).upper() + str(apiinfo['currently']['summary'][1:]).lower()).center(20) + ">"
    temperature = temperature.encode("utf-8")
    date = date.encode("utf-8")
    for elements in range(1 ,len(zed[day])):
        ser.write(date)
        ser.write(temperature)
        clas = "<"+zed[day][elements][0][0:8].center(20)+">"
        tim = "<"+ zed[day][elements][1].center(20) + ">"
        bytelines=clas.encode("ascii")
        ser.write(bytelines)
        times = tim.encode("ascii")
        ser.write(times)
        time.sleep(5)

ser.close()
from xml.dom.minidom import parse
from datetime import datetime, timedelta
import math

def getDate(filePath):
    xml = parse(filePath)
    nameList = xml.getElementsByTagName('name')
    DateAndTime = nameList[0].firstChild.data
    Date = DateAndTime.split(' ')[0]
    return Date

def getDistancesAndTimes(filePath):
    xml = parse(filePath)
    trkptList = xml.getElementsByTagName('trkpt')

    lat_A = float(trkptList[0].getAttribute('lat'))
    lon_A = float(trkptList[0].getAttribute('lon'))

    lat_A = math.radians(lat_A)
    lon_A = math.radians(lon_A)

    time_A = trkptList[0].getElementsByTagName('time')
    time_A = datetime.strptime(time_A[0].firstChild.data, '%Y-%m-%dT%H:%M:%SZ')

    distancesList = []
    timeIntervalsList = []

    for trkpt in trkptList:

        lat_B = float(trkpt.getAttribute('lat'))
        lon_B = float(trkpt.getAttribute('lon'))

        lat_B = math.radians(lat_B)
        lon_B = math.radians(lon_B)

        time_B = trkpt.getElementsByTagName('time')
        time_B = datetime.strptime(time_B[0].firstChild.data, '%Y-%m-%dT%H:%M:%SZ')

        val_temp = math.cos(lat_A) * math.cos(lat_B) * math.cos(lon_A - lon_B) + math.sin(lat_A) * math.sin(lat_B)

        try:
            dist = 6378137 * math.acos(val_temp)
        except ValueError:
            dist = 6378137 * math.acos(1)

        distancesList.append(dist)
        timeIntervalsList.append(time_B-time_A)

        lat_A = lat_B
        lon_A = lon_B
        time_A = time_B

    distancesList.pop(0)
    timeIntervalsList.pop(0)

    return distancesList, timeIntervalsList

def getSummaryDistance(distancesList):
    SummaryDistance = 0
    for dist in distancesList:
        SummaryDistance += dist
    SummaryDistance = math.ceil(SummaryDistance/10) / 100
    return SummaryDistance

def getSummaryTime(timeIntervalsList):
    SummaryTime = timedelta()
    for time in timeIntervalsList:
        SummaryTime += time
    return SummaryTime

def getAvgSpeed(SummaryDistance, SummaryTime):
    one_hour = timedelta(0,0,0,0,0,1)
    AvgSpeed = SummaryDistance / (SummaryTime / one_hour)
    AvgSpeed = math.ceil (AvgSpeed * 100) / 100
    return AvgSpeed

def getAvgPace(SummaryDistance, SummaryTime):
    AvgPace = SummaryTime / SummaryDistance
    AvgPace = AvgPace - timedelta (0, 0, AvgPace.microseconds)
    return AvgPace

def getPacesOneKm(distancesList, timeIntervalsList):
    i = 0
    temp_dist = 0
    temp_time = timedelta()
    paceList = []
    while i < len(distancesList):
        temp_dist += distancesList[i]
        temp_time += timeIntervalsList[i]
        if temp_dist > 1000:
            paceList.append(temp_time)
            temp_dist = 0
            temp_time = timedelta()
        if i == (len(distancesList) - 1):
            try:
                last_val = temp_time/(temp_dist/1000)
                last_val = last_val - timedelta (0, 0, last_val.microseconds)
                paceList.append(last_val)
            except ZeroDivisionError:
                last_val = 0
        i += 1
    return paceList

def getAvgSpeedPerKm(paceList):
    one_hour = timedelta(0,0,0,0,0,1)
    avgSpeedList = [one_hour/pace for pace in paceList]
    avgSpeedList = [math.ceil(item*100)/100 for item in avgSpeedList]
    return avgSpeedList
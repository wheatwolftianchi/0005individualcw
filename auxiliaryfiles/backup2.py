from abc import ABC, abstractmethod  
import timeit

class AbstractLondonRailwayMapper(ABC):
    
    # constructor
    @abstractmethod
    def __init__(self):
        pass           
        
    # data initialisation
    @abstractmethod
    def loadStationsAndLines(self):
        pass

    # returns the minimum number of stops to connect station "fromS" to station  "toS"
    # fromS : str
    # toS : str
    # numStops : int
    @abstractmethod
    def minStops(self, fromS, toS):     
        numStops = -1
        return numStops    
    
    # returns the minimum distance in miles to connect station "fromS" to station  "toS"
    # fromS : str
    # toS : str
    # minDistance : float
    @abstractmethod
    def minDistance(self, fromS, toS):
        minDistance = -1.0
        return minDistance
    
    # given an unordered list of station names, returns a new railway line 
    # (represented as a list of adjacent station names), connecting all such stations 
    # and such that the sum of the distances (in miles) between adjacent stations is minimised
    # inputList : set<str>
    # outputList : list<str>
    @abstractmethod
    def newRailwayLine(self, inputList):
        outputList = []
        return outputList

import math

class Station:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.relation = {}
        self.line = []

    def rad(self, d):
        return d * math.pi / 180.0

    def getDistance(self, station):
        EARTH_REDIUS = 6371.004 #km average radius
        latself = float(self.latitude)
        latstation = float(station.latitude)
        lonself = float(self.longitude)
        lonstation = float(station.longitude)
        C = math.sin(latstation)*math.sin(latself) + math.cos(latstation)*math.cos(latself)*math.cos(lonstation - lonself)
        radLat1 = self.rad(latself)
        radLat2 = self.rad(latstation)
        a = radLat1 - radLat2
        b = self.rad(lonself) - self.rad(lonstation)
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
        s = s * EARTH_REDIUS
        
        return s

    def addRelation(self, station):
        if station.name not in self.relation.keys():
            distance = self.getDistance(station)
            self.relation[station.name] = distance
            station.relation[self.name] = distance

    def addLineinfo(self, linename):
        if linename not in self.line:
            self.line.append(linename)
    
class Network:
    def __init__(self):
        self.stations = {}
    
    def addStation(self, name, latitude, longitude):
        if name not in self.stations.keys():
            station = Station(name, latitude, longitude)
            self.stations[name] = station
    
    def addLine(self, stationA, stationB, linename):
        stationA.addRelation(stationB)
        stationA.addLineinfo(linename)
        stationB.addLineinfo(linename)

    def getStation(self, name):
        return self.stations.get(name)

import csv
import random
import math

class LondonRailwayMapper(AbstractLondonRailwayMapper):

    def __init__(self):
        # ADD YOUR CODE HERE
        self.railwayNetwork = self.loadStationsAndLines()
            
     

    def loadStationsAndLines(self):
        # ADD YOUR CODE HERE
        railwayNetwork = Network()
        csvFilestations = open("londonstations.csv", "r")
        csvFilerailwaylines = open("londonrailwaylines.csv", "r")
        reader0 = csv.reader(csvFilestations)
        reader1 = csv.reader(csvFilerailwaylines)
        csvFilestations.readline()
        csvFilerailwaylines.readline()
        for row in reader0:
            railwayNetwork.addStation(row[0], row[1], row[2])
        csvFilestations.close()

        for row in reader1:
            stationA = railwayNetwork.getStation(row[1])
            stationB = railwayNetwork.getStation(row[2])
            railwayNetwork.addLine(stationA, stationB, row[0])
        
        return railwayNetwork
        
        
    

    def minStops(self, fromS, toS):     
        numStops = -1
        # ADD YOUR CODE HERE
        toStation = self.railwayNetwork.getStation(toS)
        queue = {}
        queue[fromS] = 0
        seen = set()
        seen.add(fromS)
        parent = {fromS:None}
        minimum = {}
        previous = fromS
        for station in self.railwayNetwork.stations.keys():
            minimum[station] = 114514
        minimum[fromS] = 0
        while len(queue) > 0:
            queue = dict(sorted(queue.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
            vertex = queue.popitem()
            vertexName = vertex[0]
            nodes = self.railwayNetwork.getStation(vertexName).relation.keys()
            if vertexName == fromS:
                stops = minimum.get(previous)
            else:
                stops = minimum.get(parent.get(vertexName)[0]) + 1

            if minimum[vertexName] > stops:
                minimum[vertexName] = stops
            if toS in nodes:
                return minimum.get(vertexName)
            for station in nodes:
                if station not in seen:
                    score = stops #self.railwayNetwork.getStation(station).getDistance(toStation) + stops
                    queue[station] = score
                    seen.add(station)
                    parent[station] = vertex
                if toS in self.railwayNetwork.getStation(station).relation.keys():
                    return minimum.get(parent.get(station)[0]) + 2
            previous = vertexName
            
    
        return numStops    
    
    
    
    def minDistance(self, fromS, toS):
        minDistance = -1.0
        # ADD YOUR CODE HERE
        toStation = self.railwayNetwork.getStation(toS)
        queue = {}
        queue[fromS] = 0
        seen = set()
        seen.add(fromS)
        parent = {fromS:None}
        minimum = {}
        previous = fromS
        for station in self.railwayNetwork.stations.keys():
            minimum[station] = 1145141919810
        minimum[fromS] = 0
        while len(queue) > 0:
            queue = dict(sorted(queue.items(), key = lambda kv:(kv[1], kv[0]), reverse=True))
            vertex = queue.popitem()
            vertexName = vertex[0]
            nodes = self.railwayNetwork.getStation(vertexName).relation.keys()
            if vertexName == fromS:
                stops = minimum.get(previous)
            else:
                stops = minimum.get(parent.get(vertexName)[0]) + self.railwayNetwork.getStation(parent.get(vertexName)[0]).getDistance(self.railwayNetwork.getStation(vertexName))

            if minimum[vertexName] == 1145141919810:
                minimum[vertexName] = stops
            #if toS in nodes:
                #return minimum.get(vertexName)*0.62137
            for station in nodes:
                if station not in seen:
                    score = self.railwayNetwork.getStation(station).getDistance(toStation) + stops + self.railwayNetwork.getStation(station).relation.get(vertexName)
                    queue[station] = score
                    seen.add(station)
                    parent[station] = vertex
                if toS in self.railwayNetwork.getStation(station).relation.keys():
                    return (minimum.get(parent.get(station)[0]) + self.railwayNetwork.getStation(station).relation.get(parent.get(station)[0]) + self.railwayNetwork.getStation(station).relation.get(toS))*0.62137
            previous = vertexName
        
        return minDistance
        
    
    
    def newRailwayLine(self, inputList):
        outputList = []
        # ADD YOUR CODE HERE
        inuse = inputList.copy()
        
        #inuse.reverse()
        temperature = 10000
        decreaseFactor = 0.999
        numrange = 50000
        
        
        random.shuffle(inuse)
        
        distanceA = 0
        samecounter = 0
        for i in range(len(inuse)):
            if i < len(inuse) - 1:
                distanceA += self.railwayNetwork.getStation(inuse[i]).getDistance(self.railwayNetwork.getStation(inuse[i+1]))
        for num in range(numrange):
            changelist = inuse.copy()
            countA = 0
            countB = 0
            distanceB = 0
            while countA == countB:
                countA = random.randint(0,len(inuse)-1)
                countB = random.randint(0,len(inuse)-1)
            if countA > countB:
                temp = changelist[countB]
                changelist[countB] = changelist[countA]
                changelist[countA] = temp
            else:
                temp = changelist[countA]
                changelist[countA] = changelist[countB]
                changelist[countB] = temp
            for i in range(len(changelist)):
                if i < len(changelist) - 1:
                    distanceB += self.railwayNetwork.getStation(changelist[i]).getDistance(self.railwayNetwork.getStation(changelist[i+1]))
            if distanceA > distanceB:
                inuse = changelist.copy()
                distanceA = distanceB
                samecounter = 0
                
                
            else:
                p = math.exp((distanceA - distanceB)/temperature)
                r = random.random()
                if p > r:
                    inuse = changelist.copy()
                    distanceA = distanceB
                    samecounter = 0
                    
                    
                else:
                    
                    samecounter += 1
                    if samecounter >= 1000:
                        
                        print(distanceA)
                        print(num)
                        print(temperature)
                        outputList = inuse.copy()
                        outputList.append(distanceA)
                        return outputList
            temperature = temperature*decreaseFactor
        outputList.append(distanceA)    
        print(distanceA)
        outputList = inuse
        
        



        
        return outputList

test = LondonRailwayMapper()
testMapper = LondonRailwayMapper()
fromList = ["Baker Street", "Epping", "Canonbury", "Vauxhall"]
toList = ["North Wembley", "Belsize Park", "Balham", "Leytonstone"]
'''
for i in range(len(fromList)):
    print("From", fromList[i], "to", toList[i])
    minS = test.minStops(fromList[i], toList[i])
    minD = test.minDistance(fromList[i], toList[i])
    print("minStops:\t", minS)
    print("minDistance:\t", minD)
    print("\n")
    '''
for i in range(len(fromList)):
    starttime = timeit.default_timer()
    stops = testMapper.minStops(fromList[i], toList[i])
    endtime = timeit.default_timer()
    print("\nExecution time minStops:", round(endtime-starttime,3))

    starttime = timeit.default_timer()
    dist = testMapper.minDistance(fromList[i], toList[i])
    endtime = timeit.default_timer()
    print("Execution time minDistance:", round(endtime-starttime,3))

    print("From", fromList[i], "to", toList[i], "in", stops, "stops and", dist, "miles")  
    
'''
stationsList = ["Queens Park", "Chigwell", "Moorgate", "Swiss Cottage", "Liverpool Street", "Highgate"]
starttime = timeit.default_timer()
newLine = testMapper.newRailwayLine(stationsList)
endtime = timeit.default_timer()

print("\n\nStation list", stationsList)
print("New station line", newLine)
print("Total track length from", newLine[0], "to", newLine[len(newLine)-1], ":", testMapper.minDistance(newLine[0], newLine[len(newLine)-1]), "miles")
print("Execution time newLine:", round(endtime-starttime,3))
'''
#
# testing the newRailwayLine() API on a big list of stations  
#
stationsList = ["Abbey Road", "Barbican", "Bethnal Green", "Cambridge Heath", "Covent Garden", "Dollis Hill", "East Finchley", "Finchley Road and Frognal", "Great Portland Street", "Hackney Wick", "Isleworth", "Kentish Town West", "Leyton", "Marble Arch", "North Wembley", "Old Street", "Pimlico", "Queens Park", "Richmond", "Shepherds Bush", "Tottenham Hale", "Uxbridge", "Vauxhall", "Wapping"]

starttime = timeit.default_timer()
newLine = testMapper.newRailwayLine(stationsList)
endtime = timeit.default_timer()

print("\n\nStation list", stationsList)
print("New station line", newLine)
#print("Total track length from", newLine[0], "to", newLine[len(newLine)-1], ":", testMapper.minDistance(newLine[0], newLine[len(newLine)-1]), "miles")
print("Execution time newLine:", round(endtime-starttime,3))


mindistset = []
mindistnum = 0
max = 0
min = 113123123
for i in range(100):
    current = float(testMapper.newRailwayLine(stationsList)[len(stationsList)])
    mindistnum += current
    if current > max:
        max = current
    if current < min:
        min = current
    #mindistset.append(newLine[0])
mindistnum = mindistnum/100
print("max:",max)
print("min:",min)
print("average",mindistnum)

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

    def getDistance(self, station):
        earthRadius = 6371.004 #km average radius
        latself = float(self.latitude)
        latstation = float(station.latitude)
        lonself = float(self.longitude)
        lonstation = float(station.longitude)
        C = math.sin(latstation)*math.sin(latself) + math.cos(latstation)*math.cos(latself)*math.cos(lonstation - lonself)
        
        return earthRadius * math.acos(C)*math.pi/180.0

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
                    score = self.railwayNetwork.getStation(station).getDistance(toStation) + stops
                    queue[station] = score
                    seen.add(station)
                    parent[station] = vertex
                if toS in self.railwayNetwork.getStation(station).relation.keys():
                    return minimum.get(parent.get(station)[0]) + 1
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

            if minimum[vertexName] > stops:
                minimum[vertexName] = stops
            if toS in nodes:
                return minimum.get(vertexName)*0.62137
            for station in nodes:
                if station not in seen:
                    score = self.railwayNetwork.getStation(station).getDistance(toStation) + stops
                    queue[station] = score
                    seen.add(station)
                    parent[station] = vertex
                if toS in self.railwayNetwork.getStation(station).relation.keys():
                    return (minimum.get(parent.get(station)[0]) + self.railwayNetwork.getStation(station).relation.get(parent.get(station)[0]))*0.62137
            previous = vertexName
        
        return minDistance
        
    
    
    def newRailwayLine(self, inputList):
        outputList = []
        # ADD YOUR CODE HERE

        
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
    
'''
Author
---------
Iddriss Raaj (2022)

Summary
--------
Find the optimal route given source location and final destination
'''
import csv
import helpers as hp

# Database dir
airlineDb = "db/airlines.csv"
airportsDb = "db/airports.csv"
routesDb = "db/routes.csv"

# gets and return a list of Airports in a country based on the city from airports db


def getAirports(city="", country="", id=""):
    stripCity = city.strip()
    striptCountry = country.strip()

    airportList = []

    with open(airportsDb, newline='') as airports:
        data = csv.reader(airports)

        if city != "" and country != "":
            print(
                f"=> locating all airports in {stripCity}, {striptCountry} ....")
            # filter airports based on city and country to get the airpot IDs
            for airport in filter(lambda x: stripCity in x and striptCountry in x, data):
                airportList.append(airport)
        elif id != "":
            airportList.extend(filter(lambda x: id == x[0] or id ==x[4], data))

    return airportList

# compute and return total distance covered using the Haversine formular


def totalDistance(radius, routes):
    totalDistance = 0

    print("=> calculating total distance ....")
    for route in routes:
        sourceID = route[2] if (route[3] in '\\N') else route[3]
        destinationID = route[4] if (route[5] in '\\N') else route[5]

        try:
            starAirport = getAirports(id=sourceID)[0]
            stopAirport = getAirports(id=destinationID)[0]
        except IndexError:
                return 0

        lat1 = float(starAirport[6]) if starAirport[6] != "" else 0
        long1 = float(starAirport[7]) if starAirport[7] != "" else 0

        lat2 = float(stopAirport[6]) if stopAirport[6] != "" else 0
        long2 = float(stopAirport[7]) if stopAirport[7] != "" else 0

        if lat1 != 0 and lat2 != 0 and long1 != 0 and long2 != 0:
            distance = hp.haverSine(radius, long1, lat1, long2, lat2)

            totalDistance += distance

    return totalDistance

# gets and returns all active airlines based on ID


def getActiveAirlines(airlineIDs):
    print(f"=> finding active airlines....")
    activeAirlines = []

    for id in airlineIDs:
        with open(airlineDb, newline="") as airlines:
            data = csv.reader(airlines)
            activeAirlines += filter(lambda x: id ==
                                     x[0] and x[7] == "Y", data)

    return activeAirlines

# get and return route as nodes using an airpot ID


def getNodes(airportID, loc=3):
    possibleNodes = []
    with open(routesDb, newline="") as routes:
        data = csv.reader(routes)

        allroutes = []
        airlinesInAirport = []
        for i in filter(lambda x: airportID in x and x.index(airportID) == loc, data):
            allroutes.append(i)
            if i[1] in airlinesInAirport:
                continue
            else:
                airlinesInAirport.append(i[1])
        activeAirlines = getActiveAirlines(airlinesInAirport)

        for active in activeAirlines:
            possibleNodes += filter(lambda x: x[1] in active, allroutes)
    return possibleNodes

# creates a graph of the routes from the starting airport, break immediately when 
# destination is found


def createGraph(startAirports, destAirports):
    airportIDs = hp.extractAirportID(startAirports)
    destAirportIDs = hp.extractAirportID(destAirports)
    finalGraph = {}
    
    # confirm airportIDs and destAirportIDs are not empty
    # return an empty graph
    if len(airportIDs) < 1 or len(destAirportIDs) < 1:
        return finalGraph

    for start in airportIDs:
        checked = set()
        queue = [start]
        graph = {}

        print(f"=> generating graph of possible routes from {start}")
        while queue:
            point = queue.pop(0)
            nodes = getNodes(point)
            
            if len(queue) > 2000:
                graph["done"] = False
                return graph
            
            if point not in checked:
                checked.add(point)
                graph[point] = []
                checkedDestinations = set()

                for node in nodes:
                    nde = node[4] if (node[5] in '\\N') else node[5]
                    if nde not in checkedDestinations and nde != start and nde not in checked:
                        checkedDestinations.add(nde)
                        
                        if len(node) > 0:
                            graph[point] += [node]
                        else:
                            continue

                        if nde in destAirportIDs:
                            graph["done"] = True
                            finalGraph.update(graph)
                            return finalGraph

                for node in graph[point]:
                    nde = node[4] if (node[5] in '\\N') else node[5]
                    queue.extend([nde])

        print(f"=> updating all graphs...")
        finalGraph.update(graph)
    return finalGraph

# creates a graph of the routes from the destination airport, break immediately when 
# starting point is found
def createGraphFromEnd(startAirports, destAirports):
    airportIDs = hp.extractAirportID(startAirports)
    destAirportIDs = hp.extractAirportID(destAirports)
    finalGraph = {}
    
    # confirm airportIDs and destAirportIDs are not empty
    # return an empty graph
    if len(airportIDs) < 1 or len(destAirportIDs) < 1:
        return finalGraph

    for end in destAirportIDs:
        checked = set()
        queue = [end]
        graph = {}

        print(f"=> generating graph of possible routes from {end}")
        while queue:
            point = queue.pop(0)
            nodes = getNodes(point, 5)
            
            if len(queue) > 2000:
                return graph
            
            if point not in checked:
                checked.add(point)
                graph[point] = []
                checkedDestinations = set()

                for node in nodes:
                    nde = node[2] if (node[3] in '\\N') else node[3]
                    if nde not in checkedDestinations and nde != end and nde not in checked:
                        checkedDestinations.add(nde)
                        
                        if len(node) > 0:
                            graph[point] += [node]
                        else:
                            continue

                        if nde in startAirports:
                            finalGraph.update(graph)
                            return finalGraph

                for node in graph[point]:
                    nde = node[2] if (node[3] in '\\N') else node[3]
                    queue.extend([nde])

        print(f"=> updating all graphs...")
        finalGraph.update(graph)
    return finalGraph

# returns a list of valid routes by finding the final destination,
# and using the source id of the current final destination to get the next node 


def gettRoute(routes, startAirports, destAirports):
    airportIDs = hp.extractAirportID(startAirports)
    destAirportIDs = hp.extractAirportID(destAirports)

    print("=> finding valid routes ...")
    end = False if len(routes) > 0 else True
    list = []
    counter = 0
    # trace backwards
    while not end:

        # cannot link to next route, 
        if counter > 3045146:
            return []

        for route in routes.values():

            for node in route:
                nde = node[4] if (node[5] in '\\N') else node[5]
                if nde in destAirportIDs:
                    list.append(node)
                    destAirportIDs = [list[-1][3]] if (list[-1][3] not in "\\N") else [list[-1][2]]
                    
                    # reset counter
                    counter = 0
                    if node[3] in airportIDs:
                        end = True
                else:
                    counter += 1

    return list[::-1]

# return final optimal route


def optimalRoute(start, destination):

    ## check that source is not destination
    # return empty if they are the same
    if start == destination:
        return []

    startList = getAirports(start[0], start[1])
    destList = getAirports(destination[0], destination[1])

    print("=> finding shortest route...")
    graphStart = createGraph(startList, destList)
    

    cleanGraph = {}
    
    if graphStart:
        if graphStart["done"] == False:
            graphEnd = createGraphFromEnd(startList, destList)

            graphStart.update(graphEnd)

        for (key, route) in graphStart.items():
            
            if type(route) == bool:
                continue
            if len(route) > 0 :
                cleanGraph[key] = route
                continue

    try:
        return gettRoute(cleanGraph, startList, destList)
    except StopIteration:
        return []

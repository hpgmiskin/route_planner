from shared import *
import numpy,itertools

def progressiveRoute(nodes,nodesPerRoute=4):
	"method to progressively work through the data set to plot an optimal path"

	totalRouteNodes = nodesPerRoute*2

	numberNodes = len(nodes)
	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes)

	#define list of nodes sorted by vertical location
	sortedIndexs = sorted(list(range(len(nodes))), key = lambda x:nodes[x][2])

	#assign start and end points for total route
	routeA = [sortedIndexs[0]]
	routeB = [sortedIndexs[1]]

	#work through dataset
	for i in range(0,numberNodes,2):

		nodeA = routeA[-1]
		nodeB = routeB[-1]

		#consider nodes above current
		currentIndexs = sortedIndexs[:i+totalRouteNodes]

		#remove nodes already in route
		for node in routeA[:-1]:
			currentIndexs.remove(node)
		for node in routeB[:-1]:
			currentIndexs.remove(node)

		#if there are fewer nodes left than totalRouteNodes
		if (len(currentIndexs) < totalRouteNodes):
			#find all possible routes between last node in route a and first in route b
			routes = routePermutations(currentIndexs,nodeA,nodeB)
			#compute costs for each route
			costs = [routeCost(route) for route in routes]
			#select cheapest cost
			bestCost = min(costs)
			#select corresponding route
			bestRoute = routes[costs.index(bestCost)]
			#for all items in route aside from start and end nodes add them to route a
			for index in bestRoute[1:-1]:
				routeA.append(index)
			#break the for loop as route complete
			break

		#compute the index of the highest node
		highestIndex = sorted(currentIndexs, key=lambda x:nodes[x][2])[-1]

		#calculate all possible route combinations
		possibleRoutes = doubleRoutePermutations(currentIndexs,nodeA,nodeB)
		
		#assign a default best route and cost to 
		bestRoute = possibleRoutes[0]
		bestCost = numpy.infty

		#for all possible routes check if least cost
		for route in possibleRoutes:

			costA = routeCost([i for i in route[0]]+[highestIndex])
			costB = routeCost([i for i in route[1]]+[highestIndex])
			cost = sum([costA,costB])

			#if cost is improvement assign best route and best cost
			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		bestRouteA,bestRouteB = bestRoute

		if (max([len(bestRouteA),len(bestRouteB)])>1):
			routeA.append(bestRouteA[1])
			routeB.append(bestRouteB[1])

	routeB.reverse()
	bestRoute = routeA+routeB
	bestCost = routeCost(bestRoute,True)

	return bestRoute,bestCost

def allRoutes(nodes):
	"function to compute and return all possible route combinations and the resulting costs"

	numberNodes = len(nodes)
	nodeIndexs = list(range(0,numberNodes))

	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes)

	routes,costs = [],[]
	for route in itertools.permutations(nodeIndexs):

		cost = routeCost(route,True)
		routes.append(route)
		costs.append(cost)

	return routes,costs

def allRoutesStartEnd(nodes,startIndex=None,endIndex=None):
	"function to compute and return all possible route combinations and the resulting costs"

	numberNodes = len(nodes)
	nodeIndexs = list(range(0,numberNodes))
	nodeIndexs.pop(startIndex)
	nodeIndexs.pop(endIndex)

	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes)

	routes,costs = [],[]
	for route in itertools.permutations(nodeIndexs):

		route = [startIndex]+[index for index in route]+[endIndex]

		cost = routeCost(route,True)
		routes.append(route)
		costs.append(cost)

	return routes,costs

def orderNodes(nodes,order,loop=False):
	"function to order the given nodes and return along with the final node to produce a route"

	orderedNodes = []

	for index in order:
		orderedNodes.append(nodes[index])

	if loop:
		orderedNodes.append(nodes[order[0]])

	return orderedNodes

def routeDistance(nodes,loop=False):
	"calculates the distance to navigate all nodes"

	totalDistance = 0

	for i in range(len(nodes)-1):
		vector = nodes[i+1]-nodes[i]
		distance = numpy.linalg.norm(vector)
		totalDistance += distance

	if loop:
		vector = nodes[0]-nodes[-1]
		distance = numpy.linalg.norm(vector)
		totalDistance += distance

	return totalDistance

def routeCost(route,loop=False):
	"calculates the cost of a route given a route (sequence of nodes)"

	cost = []
	for i in range(len(route)-1):
		nodeFrom = route[i]
		nodeTo = route[i+1]
		cost.append(energyMatrix[nodeFrom][nodeTo])

	if loop:
		cost.append(energyMatrix[route[-1]][route[0]])

	return sum(cost)

def setEnergyMatrix(nodes):
	"returns a matrix of energy costs to navigate the given node locations"

	numberNodes = len(nodes)
	global energyMatrix
	energyMatrix = numpy.zeros([numberNodes,numberNodes])

	for i in range(numberNodes):
		for j in range(numberNodes):
			vector = nodes[j]-nodes[i]
			distance = numpy.linalg.norm(vector)
			height = vector[2]
			energyMatrix[i][j] = calculateEnergy(distance,height)

def routePermutations(indexs,startIndex=None,endIndex=None):
	"""function to return all possible route permutations given a start and end index"""

	permutations = []
	for route in itertools.permutations(indexs):

		if startIndex:
			if (startIndex != route[0]):
				continue

		if endIndex:
			if (endIndex != route[-1]):
				continue

		permutations.append(route)

	return permutations

def doubleRoutePermutations(indexs,nodeA=None,nodeB=None):
    """function to display the possible permutation sets for 2 routes
    starting at node index nodeA and node index nodeB in set indexs"""

    numberNodes = len(indexs)

    if (numberNodes%2 != 0):
        raise ValueError("N needs to be an even number of indexs, {} is not even".format(numberNodes)) 
    routeLength = numberNodes//2

    permutationA=[]
    permutationB=[]

    for item in itertools.permutations(indexs,routeLength):

        if ((nodeA == item[0]) or (nodeA == None)):
            permutationA.append(item)
        elif ((nodeB == item[0]) or (nodeB == None)):
            permutationB.append(item)

    def checkRoutes(routeA,routeB):
        """checks the given routes to see if any indexs are repeated

        returns True if exclusive
        returns False if any repetition
        """

        for node in routeA:
            if (node in routeB):
                return False

        return True

    permutations = []

    for routeA in permutationA:
        for routeB in permutationB:

            if checkRoutes(routeA,routeB):
                permutations.append([routeA,routeB])

    return permutations
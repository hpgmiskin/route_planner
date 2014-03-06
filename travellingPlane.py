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


		highestIndex = sorted(currentIndexs, key=lambda x:nodes[x][2])[-1]

		#calculate all possible route combinations
		possibleRoutes = doubleRoutePermutations(currentIndexs,nodeA,nodeB)
		
		#print(possibleRoutes)
		bestRoute = possibleRoutes[0]
		bestCost = numpy.infity

		#for all possible routes check if least cost
		for route in possibleRoutes:

			costA = routeCost([i for i in route[0]]+[highestIndex])
			costB = routeCost([i for i in route[1]]+[highestIndex])
			cost = sum([costA,costB])

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		bestRouteA,bestRouteB = bestRoute

		if (max([len(bestRouteA),len(bestRouteB)])>1):
			routeA.append(bestRouteA[1])
			routeB.append(bestRouteB[1])

	routeB.reverse()
	bestRoute = routeA+routeB
	bestCost = routeCost(bestRoute)

	return bestRoute,bestCost

def allRoutes(nodes):
	"function to compute and return all possible route combinations and the resulting costs"

	numberNodes = len(nodes)
	nodeIndexs = list(range(0,numberNodes))

	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes)


	routes,costs = [],[]
	for route in itertools.permutations(nodeIndexs):

		cost = routeCost(route)
		routes.append(route)
		costs.append(cost)

	return routes,costs

def orderNodes(nodes,order):
	"function to order the given nodes and return"

	orderedNodes = []

	for index in order:
		orderedNodes.append(nodes[index])

	orderedNodes.append(nodes[order[0]])

	return orderedNodes

def routeCost(route):
	"calculates the cost of a route given a route (sequence of nodes)"

	cost = []
	for i in range(len(route)-1):
		nodeFrom = route[i]
		nodeTo = route[i+1]
		cost.append(energyMatrix[nodeFrom][nodeTo])

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

	#return energyMatrix

def doubleRoutePermutations(nodes,nodeA=None,nodeB=None):
    """function to display the possible permutation sets for 2 routes
    starting at node index nodeA and node index nodeB in set nodes"""

    numberNodes = len(nodes)

    if (numberNodes%2 != 0):
        raise ValueError("N needs to be an even number of nodes") 
    routeLength = numberNodes//2

    permutationA=[]
    permutationB=[]

    for item in itertools.permutations(nodes,routeLength):

        if ((nodeA == item[0]) or (nodeA == None)):
            permutationA.append(item)
        elif ((nodeB == item[0]) or (nodeB == None)):
            permutationB.append(item)

    def checkRoutes(routeA,routeB):
        """checks the given routes to see if any nodes are repeated

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
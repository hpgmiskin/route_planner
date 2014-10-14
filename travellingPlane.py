from shared import *
import numpy,itertools

def progressiveRoute(nodes,beta,nodesPerRoute=4):
	"""function to progressively work through the given nodes and
	return an approximation of the best cost route"""

	#define total nodes in subset
	totalRouteNodes = nodesPerRoute*2

	#set all nodes as numpy arrays then set energy matrix
	numberNode = len(nodes)
	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes,beta)

	#define list of nodes sorted by vertical location
	sortedIndexs = sorted(list(range(len(nodes))), key = lambda x:nodes[x][2])

	#assign start and end points for total route
	routeA = [sortedIndexs[0]]
	routeB = [sortedIndexs[1]]

	#work through all nodes in steps of two
	for i in range(0,numberNode,2):

		#select last indexs of both routes as base indexs
		indexA = routeA[-1]
		indexB = routeB[-1]

		#consider nodes above current
		currentIndexs = sortedIndexs[:i+totalRouteNodes]

		#remove nodes already in route
		for index in routeA[:-1]:
			currentIndexs.remove(index)
		for index in routeB[:-1]:
			currentIndexs.remove(index)

		#if there are 3 or less nodes left calculate the exact route
		if (len(currentIndexs) <= 3):
			#find all possible routes between last node in route a and first in route b
			routes = routePermutations(currentIndexs,indexA,indexB)
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

		#calculate all possible route combinations using even number of current indexs
		possibleRoutes = doubleRoutePermutations(currentIndexs[:2*(len(currentIndexs)//2)],indexA,indexB)
		
		#assign a default best route and cost to 
		bestRoute = possibleRoutes[0]
		bestCost = numpy.infty

		#for all possible routes check if least cost
		for route in possibleRoutes:

			#define up route A (plus route to highest node in subset)
			currentRouteA = list(route[0])+[highestIndex]
			#define down route B
			currentRouteB = [i for i in reversed(route[1])]

			#compute cost of both routes
			costA = routeCost(currentRouteA)
			costB = routeCost(currentRouteB)
			cost = sum([costA,costB])

			#if cost is improvement assign best route and best cost
			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		#decompose best route into A and B
		bestRouteA,bestRouteB = bestRoute

		#if the best routes are more than inity length add second nodes to final routes
		if (max([len(bestRouteA),len(bestRouteB)])>1):
			routeA.append(bestRouteA[1])
			routeB.append(bestRouteB[1])

	#combine routes A and B to form a single best route
	routeB.reverse()
	bestRoute = routeA+routeB
	bestCost = routeCost(bestRoute,True)

	return bestRoute,bestCost

def allRoutes(beta,nodes,startIndex=None,endIndex=None):
	"function to compute and return all possible route combinations and the resulting costs"

	#define indexs of all nodes given
	numberNodes = len(nodes)
	nodeIndexs = list(range(0,numberNodes))

	#if start node defined remove from index list
	if (startIndex != None):
		nodeIndexs.pop(startIndex)
		startIndex = [startIndex]
	else:
		startIndex = []

	#if end node defined remove from index list
	if (endIndex != None):
		nodeIndexs.pop(endIndex)
		endIndex = [endIndex]
	else:
		endIndex = []

	#set energy matrix from all nodes
	nodes = [numpy.array(node) for node in nodes]
	setEnergyMatrix(nodes,beta)

	#for all permutations append route and cost
	routes,costs = [],[]
	for route in itertools.permutations(nodeIndexs):
		route = startIndex+list(route)+endIndex
		cost = routeCost(route,True)
		routes.append(route)
		costs.append(cost)

	return routes,costs

def orderNodes(nodes,order,loop=False):
	"function to order the given nodes and return along with the final node to produce a route"

	#order nodes by order given
	orderedNodes = [nodes[index] for index in order]

	#if loop required append first node at end
	if loop: orderedNodes.append(nodes[order[0]])

	return orderedNodes

def routeCost(route,loop=False):
	"calculates the cost of a route given a route (sequence of nodes)"

	cost = 0
	#for all connections between nodes append the cost of the path
	for i in range(len(route)-1):
		nodeIndexFrom = route[i]
		nodeIndexTo = route[i+1]
		cost += energyMatrix[nodeIndexFrom][nodeIndexTo]

	#if loop required add cost of path back to start node
	if loop:
		nodeIndexFrom = route[-1]
		nodeIndexTo = route[0]
		cost += energyMatrix[nodeIndexFrom][nodeIndexTo]

	return cost

def setEnergyMatrix(nodes,beta):
	"returns a matrix of energy costs to navigate the given node locations"

	global energyMatrix
	numberNodes = len(nodes)
	energyMatrix = numpy.zeros([numberNodes,numberNodes])

	for i in range(numberNodes):
		for j in range(numberNodes):
			vector = nodes[j]-nodes[i]
			distance = numpy.linalg.norm(vector)
			height = vector[2]
			energyMatrix[i][j] = calculateEnergy(distance,height,beta)


def routePermutations(indexs,startIndex=None,endIndex=None):
	"""function to return all possible route permutations given a start and end index"""

	#if start node defined remove from indexs
	if (startIndex != None):
		indexs.remove(startIndex)
		startIndex = [startIndex]
	else:
		startIndex = []

	#if end node defined remove from indexs
	if (endIndex != None):
		indexs.remove(endIndex)
		endIndex = [endIndex]
	else:
		endIndex = []

	#compute all possible permutations
	permutations = []
	for route in itertools.permutations(indexs):
		permutations.append(startIndex+list(route)+endIndex)

	return permutations

def doubleRoutePermutations(indexs,nodeA=None,nodeB=None):
	"""function to display the possible permutation sets for 2 routes
	starting at node index nodeA and node index nodeB in set indexs"""

	#define the number nodes and route length given the node indexs
	numberNodes = len(indexs)
	routeLength = numberNodes//2

	#if the number of nodes is not even rasise an error
	if (numberNodes%2 != 0):
		raise ValueError("N needs to be an even number of indexs, {} is not even".format(numberNodes)) 

	#for all potential permutations of length N/2 in N indexs 
	permutationA,permutationB = [],[]
	for item in itertools.permutations(indexs,routeLength):
		#if nodeA is the start node or nodeA is none append to permuatonA
		if ((nodeA == item[0]) or (nodeA == None)):
			permutationA.append(item)
		#if nodeB is the start node or nodeB is none append to permuatonB
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

	#for all combinations of sub routes
	permutations = []
	for routeA in permutationA:
		for routeB in permutationB:
			#if the combination is exclusive append to final permutations
			if checkRoutes(routeA,routeB):
				permutations.append([routeA,routeB])

	return permutations

def routeData(nodes,beta,loop=False):
	"function to return the route data of the given node ordering"

	distances,heights,costs = [],[],[]

	def distanceHeightCost(nodeFrom,nodeTo):
		"returns the distance,height and cost for travel between nodes"

		vector = nodes[i+1]-nodes[i]
		distance = numpy.linalg.norm(vector)
		height = vector[2]
		cost = calculateEnergy(distance,height,beta)

		return distance,height,cost

	for i in range(len(nodes)-1):
		nodeFrom = nodes[i]
		nodeTo = nodes[i+1]
		distance,height,cost = distanceHeightCost(nodeFrom,nodeTo)

		distances.append(distance)
		heights.append(height)
		costs.append(cost)

	if loop:
		nodeFrom = nodes[-1]
		nodeTo = nodes[0]
		distance,height,cost = distanceHeightCost(nodeFrom,nodeTo)

		distances.append(distance)
		heights.append(height)
		costs.append(cost)

	heights = [abs(height) for height in heights]
	glideHeight = sum([height for i,height in enumerate(heights) if (costs[i] == 0)])
	glideDistance = sum([distance for i,distance in enumerate(distances) if (costs[i] == 0)])

	totalHeight = sum(heights)
	totalDistance = sum(distances)
	totalCost = sum(costs)

	data = {
		"cost":totalCost,
		"height":totalHeight,
		"distance":totalDistance,
		"glideHeight":glideHeight,
		"glideDistance":glideDistance
	}

	return data
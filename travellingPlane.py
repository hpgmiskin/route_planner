from shared import *
from greedyTSP import *
from dubinPath import bestPath
import itertools
import numpy

radius = 0.1

class TravellingPlane():
	"""travellingPlane is used to calculate the optimum ordering of points given the node locations"""
	
	def __init__(self, orderType, routeOrPath):
		"initiates the travelling plane with the node location by defining the energy matrix"

		self.orderType = orderType
		self.routeOrPath = routeOrPath

	def setNodes(self,nodes,startNode=None):
		"sets the position of the nodes that travelling plane routes around and define the energy matrix"

		self.startNode=startNode
		self.numberNodes = len(nodes)
		self.nodes = [numpy.array(node) for node in nodes]
		
		if (self.routeOrPath == "route"):
			self.setEnergyMatrix()
		elif (self.routeOrPath == "path"):
			self.setEnergyPathMatrix()

	def getOrder(self,orderType=None):
		"returns the order of the nodes using the required function"

		if (orderType):
			self.orderType = orderType

		orderType = self.orderType

		if (orderType == "exact"):
			return self.exactOrder()
		elif (orderType == "greedy"):
			return self.greedyOrder()
		elif (orderType == "progressive"):
			return self.progressiveOrder()
		else:
			return None

	def progressiveOrder(self):
		"method to progressively work through the data set to plot an optimal path"

		N=8

		nodes = self.nodes
		numberNodes = self.numberNodes

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
			currentIndexs = sortedIndexs[:i+N]

			#remove nodes already in route
			for node in routeA[:-1]:
				currentIndexs.remove(node)
			for node in routeB[:-1]:
				currentIndexs.remove(node)


			highestIndex = sorted(currentIndexs, key=lambda x:nodes[x][2])[-1]

			#calculate all possible route combinations
			possibleRoutes = permutation(currentIndexs,nodeA,nodeB)
			
			#print(possibleRoutes)
			bestRoute = possibleRoutes[0]
			bestCost = 1000000

			#for all possible routes check if least cost
			for route in possibleRoutes:

				if (self.routeOrPath == "route"):
					costA = self.calculateRouteCost([i for i in route[0]]+[highestIndex])
					costB = self.calculateRouteCost([i for i in route[1]]+[highestIndex])
				elif (self.routeOrPath == "path"):
					costA = self.calculateRoutePathCost([i for i in route[0]]+[highestIndex])
					costB = self.calculateRoutePathCost([i for i in route[1]]+[highestIndex])

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

		if (self.routeOrPath == "route"):
			bestCost = self.calculateRouteCost(bestRoute)
		elif (self.routeOrPath == "path"):
			bestCost = self.calculateRoutePathCost(bestRoute)

		

		print("Progressive - {} - {:.2f}".format(bestRoute[:10],bestCost))
		return bestRoute,bestCost


	def exactOrder(self):
		"method that considers all combinations of the given route to find the optimum"

		numberNodes = self.numberNodes
		#startNode = self.startNode
		nodeIndexs = list(range(0,numberNodes))

		bestRoute = nodeIndexs

		if (self.routeOrPath == "route"):
			cost = self.calculateRouteCost(route)
		elif (self.routeOrPath == "path"):
			cost = self.calculateRoutePathCost(route)

		for i,route in enumerate(itertools.permutations(nodeIndexs)):

			if (self.routeOrPath == "route"):
				cost = self.calculateRouteCost(route)
			elif (self.routeOrPath == "path"):
				cost = self.calculateRoutePathCost(route)

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		print("Exact - {} - {:.2f}".format(bestRoute[:10],bestCost))
		return bestRoute,bestCost

	def greedyOrder(self):
		"method to find a best guess route using a suboptimal greedy travelling salesman"

		if (self.routeOrPath == "path"):
			raise ValueError("Greedy order does not allow path calculation")

		energyMatrix = self.energyMatrix

		bestRoute = solve_tsp_numpy(energyMatrix,3)
		bestCost = self.calculateRouteCost(bestRoute)

		print("Greedy - {} - {:.2f}".format(bestRoute[:10],bestCost))
		return bestRoute,bestCost

	def calculateRouteCost(self,route):
		"calculates the cost of a route given a route (ordering of nodes)"

		cost = []

		for i in range(len(route)-1):
			nodeFrom = route[i]
			nodeTo = route[i+1]
			cost.append(self.energyMatrix[nodeFrom][nodeTo])

		cost.append(self.energyMatrix[route[-1]][route[0]])
		return sum(cost)

	def calculateRoutePathCost(self,route):
		"calculates the cost of a route given a route (ordering of nodes)"

		cost = []

		for i in range(len(route)-2):
			nodeA = route[i]
			nodeB = route[i+1]
			nodeC = route[i+2]
			cost.append(self.energyPathMatrix[nodeA][nodeB][nodeC])

		cost.append(self.energyPathMatrix[route[-2]][route[-1]][route[0]])
		cost.append(self.energyPathMatrix[route[-1]][route[0]][route[1]])

		return sum(cost)

	def setEnergyMatrix(self):
		"returns a matrix of energy costs to navigate the given node locations"

		#number of nodes
		nodes = self.nodes
		numberNodes = self.numberNodes

		energyMatrix = numpy.zeros([numberNodes,numberNodes])

		for i in range(numberNodes):
			for j in range(numberNodes):
				vector = nodes[j]-nodes[i]
				distance = numpy.linalg.norm(vector)
				height = vector[2]
				energyMatrix[i][j] = calculateEnergy(distance,height)

		self.energyMatrix = energyMatrix

	def setEnergyPathMatrix(self):
		"method to set the energy matrix that takes into account change in direction"

		#number of nodes
		nodes = self.nodes
		numberNodes = self.numberNodes

		#preallocate energy path matrix
		pathMatrix = numpy.zeros([numberNodes,numberNodes,numberNodes])
		energyPathMatrix = numpy.zeros([numberNodes,numberNodes,numberNodes])

		#for set of 3 nodes
		for i in range(numberNodes):
			for j in range(numberNodes):
				for k in range(numberNodes):
					startPoint = nodes[i]
					endPoint = nodes[j]
					startDirection = nodes[j]-nodes[i]
					endDirection = nodes[k]-nodes[j]
					
					if not ((i==j) or (i==k) or (j==k)):
						pathType,energy = bestPath(startPoint,startDirection,endPoint,endDirection,radius)
					else:
						pathType,energy = None,0

					#pathMatrix[i][j][k] = pathType
					energyPathMatrix[i][j][k] = energy

		self.pathMatrix = pathMatrix
		self.energyPathMatrix = energyPathMatrix

if __name__ == "__main__":
	travellingPlane = TravellingPlane([[0,0,0],[0,1,1],[0,1,0],[0,0,1]])
	travellingPlane.getOrder()
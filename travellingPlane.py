from shared import *
from greedyTSP import *
import itertools
import numpy

class TravellingPlane():
	"""travellingPlane is used to calculate the optimum ordering of points given the node locations"""
	
	def __init__(self, orderType):
		"initiates the travelling plane with the node location by defining the energy matrix"

		self.orderType = orderType

	def setNodes(self,nodes,startNode=None):
		"sets the position of the nodes that travelling plane routes around and define the energy matrix"

		self.nodes = nodes
		self.startNode=startNode
		self.numberNodes = len(nodes)
		self.setEnergyMatrix()

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

				costA = self.calculateRouteCost([i for i in route[0]]+[highestIndex])
				costB = self.calculateRouteCost([i for i in route[1]]+[highestIndex])

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
		bestCost = self.calculateRouteCost(bestRoute)

		print("Progressive - {} - {:.2f}".format(bestRoute[:10],bestCost))
		return bestRoute,bestCost


	def exactOrder(self):
		"method that considers all combinations of the given route to find the optimum"

		numberNodes = self.numberNodes
		#startNode = self.startNode
		nodeIndexs = list(range(0,numberNodes))

		bestRoute = nodeIndexs
		bestCost = self.calculateRouteCost(nodeIndexs)

		for i,route in enumerate(itertools.permutations(nodeIndexs)):

			# if (startNode != None):
			# 	if (route[0] == startNode):
			# 		pass
			# 	else:
			# 		continue

			cost = self.calculateRouteCost(route)

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		print("Exact - {} - {:.2f}".format(bestRoute[:10],bestCost))
		return bestRoute,bestCost

	def greedyOrder(self):
		"method to find a best guess route using a suboptimal greedy travelling salesman"

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

	def setEnergyMatrix(self):
		"returns a matrix of energy costs to navigate the given node locations"

		#number of nodes
		nodes = self.nodes
		numberNodes = self.numberNodes

		energyMatrix = numpy.zeros([numberNodes,numberNodes])

		for i in range(numberNodes):
			for j in range(numberNodes):
				deltaX = nodes[j][0]-nodes[i][0]
				deltaY = nodes[j][1]-nodes[i][1]
				deltaZ = nodes[j][2]-nodes[i][2]
				energyMatrix[i][j] = calculateEnergy(deltaX,deltaY,deltaZ)

		self.energyMatrix = energyMatrix

if __name__ == "__main__":
	travellingPlane = TravellingPlane([[0,0,0],[0,1,1],[0,1,0],[0,0,1]])
	travellingPlane.getOrder()
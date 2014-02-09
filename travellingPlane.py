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
		else:
			return None
		
	def exactOrder(self):
		"selects the shortest route given the routes provided"

		numberNodes = self.numberNodes
		startNode = self.startNode
		nodeIndexs = list(range(0,numberNodes))

		bestRoute = nodeIndexs
		bestCost = self.calculateRouteCost(nodeIndexs)

		for i,route in enumerate(itertools.permutations(nodeIndexs)):

			if (startNode != None):
				if (route[0] == startNode):
					pass
				else:
					continue

			cost = self.calculateRouteCost(route)

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		print("Exact - {} - {}".format(bestRoute,bestCost))
		return bestRoute

	def greedyOrder(self):
		"method to return the order given the greedyTSP"

		energyMatrix = self.energyMatrix
		startNode = self.startNode

		if False:#(startNode != None):
			print("greedy remove node {}".format(startNode))
			energyMatrix = numpy.delete(energyMatrix, (startNode), axis=0)
			energyMatrix = numpy.delete(energyMatrix,(startNode), axis=1)

		bestRoute = solve_tsp_numpy(energyMatrix,3)
		bestCost = self.calculateRouteCost(bestRoute)

		print("Greedy - {} - {}".format(bestRoute,bestCost))
		return bestRoute

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
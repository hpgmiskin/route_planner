from shared import *
from routeOptions import RouteOptions
from itertools import permutations
import numpy

class TravellingPlane():
	"""travellingPlane is used to calculate the optimum ordering of points given the node locations"""
	
	def __init__(self, nodes):
		"initiates the travelling plane with the node location by defining the nergy matrix"

		self.nodes = nodes
		self.numberNodes = len(nodes)

		self.setEnergyMatrix()
		
	def getOrder(self):
		"selects the shortest route given the routes provided"

		numberNodes = self.numberNodes
		nodeIndexs = range(0,numberNodes)

		bestRoute = nodeIndexs
		bestCost = self.calculateRouteCost(nodeIndexs)

		for i,route in enumerate(permutations(nodeIndexs)):

			cost = self.calculateRouteCost(route)

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		print("{}".format(bestRoute))

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
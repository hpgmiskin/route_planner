from shared import *
from routeOptions import RouteOptions

import numpy

class TravellingPlane():
	"""travellingPlane is used to calculate the optimum ordering of points given the node locations"""
	
	def __init__(self, nodes):
		"initiates the travelling plane with the node location by defining the nergy matrix"

		self.nodes = nodes
		self.numberNodes = len(nodes)

		self.setEnergyMatrix()
		self.setRouteOptions()
		
	def getOrder(self):
		"selects the shortest route given the routes provided"

		routeOptions = self.routeOptions
		numberRouteOptions = len(routeOptions)

		index,total = 0,10
		progress = [int(i*numberRouteOptions/total) for i in range(total)]

		for i,route in enumerate(routeOptions):
			cost = self.calculateRouteCost(route)

			if (i == 0):
				bestRoute = route
				bestCost = cost

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

			if (i in progress):
				print("{0:02d}/{1:02d} - {2:s}".format(index,total,bestRoute))
				index += 1

		print("{0:02d}/{1:02d} - {2:s}".format(10,10,bestRoute))

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

	def setRouteOptions(self):
		"sets the differnt routes that are avialable given then number of nodes"

		self.routeOptions = RouteOptions(self.numberNodes).getRoute()

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
from shared import *
from routeOptions import RouteOptions

import numpy

class TravellingPlane():
	"""travellingPlane is used to calculate the optimum ordering of points given the node locations"""
	
	def __init__(self, nodes):
		"initiates the travelling plane with the node location by defining the nergy matrix"

		numberNodes = len(nodes)

		self.setEnergyMatrix(nodes)
		self.setRouteOptions(numberNodes)
		
	def getOrder(self):
		"selects the shortest route given the routes provided"

		routeOptions = self.routeOptions

		for i,route in enumerate(routeOptions):
			cost = self.calculateRouteCost(route)

			if (i == 0):
				bestRoute = route
				bestCost = cost

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

			if ((i/1000) == (i//1000)):
				print("{}/{}".format(i,len(routeOptions)))

		print("Route {} seleted at cost of {}".format(bestRoute,bestCost))

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

	def setRouteOptions(self,numberNodes):
		"sets the differnt routes that are avialable given then number of nodes"

		self.routeOptions = RouteOptions(numberNodes).getRoute()

	def setEnergyMatrix(self,nodes):
		"returns a matrix of energy costs to navigate the given node locations"

		#number of nodes
		N = len(nodes)
		print(nodes)

		energyMatrix = numpy.zeros([N,N])

		for i in range(N):
			for j in range(N):
				deltaX = nodes[j][0]-nodes[i][0]
				deltaY = nodes[j][1]-nodes[i][1]
				deltaZ = nodes[j][2]-nodes[i][2]
				energyMatrix[i][j] = calculateEnergy(deltaX,deltaY,deltaZ)

		self.energyMatrix = energyMatrix
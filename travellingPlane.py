import energyMatrix#.createMatrix as createMatrix
import routeOptions#.RouteOptions as RouteOptions

nodes = [[0,0,0],[0,1,0],[0,1,1],[0,0,1]]
nodes = [[0,0,0],[0,1,0],[0,1,1],[0,0,1]]
energyMatrix = energyMatrix.createMatrix(nodes)

routes = routeOptions.RouteOptions(4).getRoute()

print(energyMatrix)
print(routes)

class travellingPlane():
	"""docstring for travellingPlane"""
	
	def __init__(self, energyMatrix):
		"initiate class variables"

		self.energyMatrix = energyMatrix
		

	def selectBestRoute(self,routes):
		"selects the shortest route given the routes provided"

		for i,route in enumerate(routes):
			cost = calculateRouteCost(route)

			if (i == 0):
				bestRoute = route
				bestCost = cost

			if (cost<bestCost):
				bestRoute = route
				bestCost = cost

		return bestRoute,bestCost

	def calculateRouteCost(self,route):
		"calculates the cost of a route given a route (ordering of nodes)"

		cost = []

		for i in range(len(route)-1):
			nodeFrom = route[i]
			nodeTo = route[i+1]
			cost.append(self.energyMatrix[nodeFrom-1][nodeTo-1])

		cost.append(self.energyMatrix[route[-1]-1][route[0]-1])

		return sum(cost)
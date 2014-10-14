#pure logic for the report
from shared import *
import texDocument,latinHypercube,travellingPlane,dubinPath,planeEnergy,airFoil,nodeResults,buildModel,plot,time

def calculateEnergyModelResults(foilName,mass,wingSpan,wingArea,oswaldFactor,maxVelocity):
	"method to calculate the results to the energy model"

	currentPlane = planeEnergy.PlaneEnergy(mass,wingSpan,wingArea,oswaldFactor)

	maxRangeVelocity = float(currentPlane.setAirFoil(foilName))
	maxRangeEnergyCoff = float(currentPlane.getEnergyCoefficient())
	velocitys,series = [float(i) for i in numpy.linspace(1,maxVelocity,100)],{}
	for velocity in velocitys:
		reynoldsNumber = currentPlane.setFlightVelocity(velocity)

		if reynoldsNumber:
			seriesName = "Reynolds Number {}".format(reynoldsNumber)
			energyCoff = float(currentPlane.getEnergyCoefficient())
			if (seriesName in series.keys()):
				series[seriesName][0].append(velocity)
				series[seriesName][1].append(energyCoff)
			else:
				series[seriesName] = [[],[]]

	return {"maxRangeVelocity":maxRangeVelocity,"maxRangeEnergyCoff":maxRangeEnergyCoff,"series":series}

def calculateExactRouteResults(beta,numberOfNode,saveCosts=False):
	"computes the results to the exact TSP problem and returns all results in a dictionary"

	data = {"numberOfNode":numberOfNode}
	#load latin hypercube of given nodes
	nodes = latinHypercube.unitCube(numberOfNode)
	#define start and end nodes
	sortedNodes = sorted(nodes,key=lambda x:x[2])
	startIndex = [i for i,node in enumerate(nodes) if all([node[j]==sortedNodes[0][j] for j in range(3)])][0]
	#endIndex = [i for i,node in enumerate(nodes) if all([node[j]==sortedNodes[1][j] for j in range(3)])][0]
	#time how long it takes to calculate all routes
	tic = time.time()
	routes,costs = travellingPlane.allRoutes(beta,nodes,startIndex)#,endIndex)
	toc= time.time()
	#compute best route and cost
	bestCost = min(costs)
	bestRoute = routes[costs.index(bestCost)]

	if saveCosts:
		data["costs"] = costs

	data["bestCost"] = bestCost
	data["bestRoute"] = bestRoute
	#save results
	data["numberOfRoute"]= (len(costs))
	data["computeTime"] = (round(toc-tic,3)*1000)
	data["bestCost"] = (round(bestCost,2))
	#obtain ordered nodes
	[data["x"],data["y"],data["z"]] = changeArray(travellingPlane.orderNodes(nodes,bestRoute,True))

	return data

def calculateProgressiveResults(beta,numberOfNode,nodesPerRoute):
	"computes the results to the progressive travelling plane"

	data = {"numberOfNode":numberOfNode}
	#load latin hypercube of required nodes
	nodes = latinHypercube.unitCube(numberOfNode)
	#time how long it takes to calculate route
	tic = time.time()
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,beta,nodesPerRoute)
	toc = time.time()
	nodes = travellingPlane.orderNodes(nodes,bestRoute,True)
	data["xyz"] = changeArray(nodes)
	#save computation time
	data["computeTime"] = (round(toc-tic,3)*1000)
	#save best route and cost
	data["bestRoute"] = (bestRoute)
	data["bestCost"] = (round(bestCost,2))

	return data

def calculateDubinPathResults(beta,radius,numberOfNode,nodesPerRoute):
	"computes and returns the corresponding path data"
	paths={}
	nodes = latinHypercube.unitCube(numberOfNode)
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,beta,nodesPerRoute)
	nodes = travellingPlane.orderNodes(nodes,bestRoute)
	paths["Node Order"] = changeArray(nodes)
	routeData = travellingPlane.routeData(nodes,True)
	routeDistance = routeData["distance"]

	currentPath = dubinPath.DubinPath(radius)
	for node in nodes:
		currentPath.addNode(node)
	paths["UAV Route"] = currentPath.getPath()
	pathDistance = currentPath.getDistance()

	return {"paths":paths,"routeDistance":routeDistance,"pathDistance":pathDistance}

def calculateDubinEnergyResults(numberOfNode,maxTurnRadius,flightVelocity):
	"computes and returns the energy results to the current configuration"

	beta = 0.1
	nodes = latinHypercube.sampleSpace([1000,1000,1000],numberOfNode)
	bestRoute,bestCost = travellingPlane.progressiveRoute(nodes,beta)
	nodes = travellingPlane.orderNodes(nodes,bestRoute)

	planeModel = planeEnergy.PlaneEnergy(planeEnergy.mass,planeEnergy.wingSpan,planeEnergy.wingArea,planeEnergy.oswaldFactor)
	planeModel.setAirFoil(planeEnergy.foilName)
	planeModel.setFlightVelocity(flightVelocity)

	turnRadiuses = [turnRadius for turnRadius in numpy.linspace(0,maxTurnRadius,100)]
	pathDistances,pathEnergys = [],[]
	for turnRadius in turnRadiuses:
		currentPath = dubinPath.DubinPath(turnRadius,planeModel)
		for node in nodes:
			currentPath.addNode(node)
		pathEnergys.append(float(currentPath.getEnergy()))
		pathDistances.append(float(currentPath.getDistance()))

	return {"turnRadius":turnRadiuses,"pathEnergy":pathEnergys,"pathDistance":pathDistances}

def testModelResults(beta,maxLength,maxEnergy):
	"function that test the corresponding model data and returns the results"

	numberSeries = 5
	nodesMin = ALL_NODES[0]
	nodesMax = ALL_NODES[-1]
	nodesRange = nodesMax-nodesMin
	rangeSeries = nodesRange//numberSeries
	seriesRanges,series = {},{}
	for i in range(numberSeries):
		minimum = int(nodesMin + (i/numberSeries)*nodesRange)
		maximum = int(nodesMin + ((i+1)/numberSeries)*nodesRange)
		seriesRanges["{} <= N < {}".format(minimum,maximum)] = (minimum,maximum)
		series["{} <= N < {}".format(minimum,maximum)] = [[],[]]

	i = 0
	predictionErrors = []
	while i<100:
		xLength = int(maxLength*numpy.random.rand())
		yLength = int(maxLength*numpy.random.rand())
		zLength = int(maxLength*numpy.random.rand())
		totalEnergy = int(maxEnergy*numpy.random.rand())
		numberNode = buildModel.returnNodes(beta,xLength,yLength,zLength,totalEnergy)

		if numberNode:
			nodes = latinHypercube.sampleSpace([xLength,yLength,zLength],numberNode)
			route,energy = travellingPlane.progressiveRoute(nodes,beta)
			#orderedNodes = travellingPlane.orderNodes(nodes,route)

			predictionErrors.append(abs(totalEnergy-energy)/totalEnergy)

			for name,(minimum,maximum) in seriesRanges.items():
				if ((numberNode >= minimum) and (numberNode < maximum)):
					series[name][0].append(totalEnergy)
					series[name][1].append(energy)
			i+=1

	return {"series":series,"predictionError":predictionErrors}

if (__name__ =="__main__"):
	data = calculateExactRouteResults(5)
	print(data)
	data =  calculateProgressiveResults(0.1,12,4)
	print(data)
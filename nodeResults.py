#testModel
from shared import *
import numpy,time,scipy.optimize,latinHypercube,travellingPlane,dubinPath,plot

SAMPLE_CUBE = latinHypercube.sampleSpace([MAX_LENGTH,MAX_LENGTH,MAX_LENGTH],100)
numberI = 4
SAMPLE_PLAN = [list(SAMPLE_CUBE[i//numberI])+[0.1*int((i+1)-numberI*(i//numberI))] for i in range(len(SAMPLE_CUBE)*numberI)]
# print(SAMPLE_PLAN)

def returnNodes(alpha,xLength,yLength,zLength,totalEnergy):
	"""using the calculated models this function takes the:

	Research volume as defined by xLength,yLength and zLength
	The totalEnergy that the UAV batteries contain

	And returns the number of nodes in the optimal latin hypercube"""

	#define the sample plan
	[xLengths,yLengths,zLengths,alphas] = changeArray(SAMPLE_PLAN)

	#define all alphas that are close
	alphaIndexs = [alphas.index(item) for item in alphas if round(item,1)==round(alpha,1)]

	diffList = []
	for index in alphaIndexs:
		xDiff = abs(xLength - xLengths[index])
		yDiff = abs(yLength - yLengths[index])
		zDiff = abs(zLength - zLengths[index])

		diffList.append(sum([xDiff,yDiff,zDiff]))

	minDiff = min(diffList)
	index = alphaIndexs[diffList.index(minDiff)]

	print("------------")
	print("Desired:\t{:0.0f}\t{:0.0f}\t{:0.0f}".format(xLength,yLength,zLength))
	xLength,yLength,zLength = xLengths[index],yLengths[index],zLengths[index]
	print("Actual:\t\t{:0.0f}\t{:0.0f}\t{:0.0f}".format(xLength,yLength,zLength))

	data = computeResults(alpha,xLength,yLength,zLength)

	# energys = [calculateEnergy(data["distance"][i]-data["glideDistance"][i],data["glideHeight"][i],alpha) for i in range(len(data["numberNode"]))]
	# plot.line(data["numberNode"],{"Cost":data["cost"],"Energy":energys},show=True)

	numberNode = 0
	energyDiffs = []
	for i in range(len(data["numberNode"])):
		distance = data["distance"][i]-data["glideDistance"][i]
		height = data["glideHeight"][i]
		energy = calculateEnergy(distance,height,alpha)
		energyDiff = totalEnergy - energy
		if (energyDiff >= 0):
			energyDiffs.append(energyDiff)
		else:
			energyDiffs.append(numpy.infty)

	minEnergyDiff = min(energyDiffs)

	#LP = (9:35R + 0:90)LR

	if (minEnergyDiff > 100):
		return None

	index = energyDiffs.index(minEnergyDiff)

	return data["numberNode"][index]

def computeResults(alpha,xLength,yLength,zLength):
	"function to fully investigate the resulting routes of a latin hypercube"

	filename = "results/route_path_lengths_{:0.1f}_{:0.0f}_{:0.0f}_{:0.0f}.csv".format(alpha,xLength,yLength,zLength)

	try:
		data = loadData(filename)
	except FileNotFoundError:
		data = {"numberNode":[],"alpha":[],"xLength":[],"yLength":[],"zLength":[],"glideDistance":[],"glideHeight":[],"distance":[],"height":[],"cost":[]}
		for numberNode in EVEN_RESULTS:

			nodes = latinHypercube.sampleSpace([xLength,yLength,zLength],numberNode)
			# print(len(nodes))
			route,cost = travellingPlane.progressiveRoute(nodes,alpha)
			# print(len(route))
			orderedNodes = travellingPlane.orderNodes(nodes,route)
			routeData = travellingPlane.routeData(orderedNodes,alpha)

			data["numberNode"].append(numberNode)
			data["alpha"].append(alpha)
			data["xLength"].append(xLength)
			data["yLength"].append(yLength)
			data["zLength"].append(zLength)

			for name in ["glideDistance","glideHeight","distance","height","cost"]:
				data[name].append(routeData[name])

		saveData(filename,data)

	for key,value in data.items():
		data[key] = numpy.array(value)

	return data

def computeAllModelResults(newSample=False):
	"function to compute all length width height results possible"

	filename = "sample_plan.csv"

	if newSample:
		[xLengths,yLengths,zLengths,alphas] = changeArray(SAMPLE_PLAN)

		data = {
			"alpha":alphas,
			"xLength":xLengths,
			"yLength":yLengths,
			"zLength":zLengths,
			}

		saveData(filename,data)

	while not newSample:
		data = loadData(filename)
		alpha = data["alpha"].pop(0)
		xLength = data["xLength"].pop(0)
		yLength = data["yLength"].pop(0)
		zLength = data["zLength"].pop(0)
		try:
			saveData(filename,data)
			try:
				print(alpha,xLength,yLength,zLength)
				computeResults(alpha,xLength,yLength,zLength)
			except:
				data["alpha"].insert(0,alpha)
				data["xLength"].insert(0,xLength)
				data["yLength"].insert(0,yLength)
				data["zLength"].insert(0,zLength)
				saveData(filename,data)

		except PermissionError:
			time.sleep(20)

		if (len(data["alpha"]) < 1):
			break


if (__name__ == "__main__"):

	computeAllModelResults(False)
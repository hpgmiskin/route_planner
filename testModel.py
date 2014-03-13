#testModel
import numpy
from scipy.optimize import leastsq

def testPath():
	"function to test the results of"

	return None

def testSpace(numberNodes,numberTest=100,maxLength=1000):
	"function to fully investigate the resulting routes of a latin hypercube"

	testCases = latinHypercube.sampleSpace(maxLength,maxLength,maxLength,numberTest)

	filename = "results/route_path_lengths_L_{}_N_{}_T_{}.csv".format(maxLength,numberNode,numberTest)
	try:
		data = loadData(filename)
	except FileNotFoundError:
		data = {"X":[],"Y":[],"Z":[],"Area":[],"Volume":[],"Distance":[],"Height":[],"Energy":[]}
		for testCase in testCases:
			[X,Y,Z] = testCase
			nodes = latinHypercube.sampleSpace(X,Y,Z,numberNode)
			route,energy = travellingPlane.progressiveRoute(nodes)
			orderedNodes = travellingPlane.orderNodes(nodes,route)
			distance,height = travellingPlane.routeDistance(orderedNodes)

			area = X*Y
			volume = X*Y*Z
			data["X"].append(X)
			data["Y"].append(Y)
			data["Z"].append(Z)
			data["Area"].append(area)
			data["Volume"].append(volume)
			data["Distance"].append(distance)
			data["Height"].append(height)
			data["Energy"].append(energy)

		saveData(filename,data)

	return data

def buildModel():
	"""function to build a model from a number of parameters"""

	def modelDistance(parameters, x, y, z, N):
	    m,e,mz,ez,mN,eN = parameters
	    return (m*(x**e+y**e)+mz*z**ez)*(mN*N**eN)

	def modelClimb(parameters, x, y, z, N):


	parameters = numpy.array([p0, e0, p1, e1, p2, e2])
	arguments = (y, a, b, c)
	result = leastsq(model, parameters, arguments)

	print(result)
	print('y = {:f} a^{:f} + {:f} b^{:f} {:f} c^{:f}'.format(map(float, result)))
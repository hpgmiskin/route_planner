from shared import *
import numpy,time,scipy.optimize,latinHypercube,travellingPlane,dubinPath,plot

def returnNodes(beta,xLength,yLength,zLength,totalEnergy):
	"""using the calculated models this function takes the:

	Research volume as defined by xLength,yLength and zLength
	The totalEnergy that the UAV batteries contain

	And returns the number of nodes in the optimal latin hypercube"""

	#load the results to the model calculations
	filename = "results/model_variables.csv"
	variables = loadData(filename)

	#collect nodes and betas
	numberNodes = variables["N"]
	betas = variables["A"]

	#for all numbers of nodes
	for numberNode in ALL_NODES:

		#find all indexs of nodes 
		nodeIndexs = [i for i in range(len(numberNodes)) if numberNode == numberNodes[i]]
		#find the closes beta value
		betaDiffs = [abs(beta-betas[i]) for i in nodeIndexs]
		#return the index of closest value
		index = nodeIndexs[betaDiffs.index(min(betaDiffs))]

		#set number of nodes using index to ensure correct
		N = variables["N"][index]
		A = variables["A"][index]

		#set the energy model parameters using index
		energyParameters = [
			variables["ma"][index],
			variables["ea"][index],
			variables["md"][index],
			variables["ed"][index],
			variables["mz"][index],
			variables["ez"][index],
			variables["c"][index]
			]

		#calculate distance, height and thus energy
		energy = energyModel(energyParameters,xLength,yLength,zLength)

		#if energy is more than total energy
		if (energy > totalEnergy):
			
			#if first row flight not possible therefore return None
			if (numberNode == ALL_NODES[0]):
				return None

			#take the previous value for number of nodes
			N = variables["N"][index-1]

			#end loop
			break

	if (N == ALL_NODES[-1]):
		return None

	# print(A,N,energy)
	return int(N)

def computeResults(beta,numberNode):
	"function to fully investigate the resulting routes of a latin hypercube"

	testCases = latinHypercube.sampleSpace([MAX_LENGTH,MAX_LENGTH,MAX_LENGTH],100)

	filename = "results/route_path_lengths_{:0.1f}_{:0.0f}.csv".format(beta,numberNode)

	try:
		data = loadData(filename)
	except IOError:
		data = {"X":[],"Y":[],"Z":[],"Energy":[]}
		for testCase in testCases:

			[X,Y,Z] = testCase
			nodes = latinHypercube.sampleSpace([X,Y,Z],numberNode)
			route,energy = travellingPlane.progressiveRoute(nodes,beta)
			orderedNodes = travellingPlane.orderNodes(nodes,route)
			routeData = travellingPlane.routeData(orderedNodes,beta)

			data["X"].append(X)
			data["Y"].append(Y)
			data["Z"].append(Z)
			data["Energy"].append(energy)

		saveData(filename,data)

	return data

def energyModel(parameters,x,y,z):
	ma,ea,md,ed,mz,ez,c = parameters

	return ma*(x*y)**ea + md*numpy.abs(x-y) + mz*z**ez + c

def returnModel(beta,numberNode):
	"computes a model for length width and height given the number of nodes"

	def collectResults():
		"function to collect all results of the space analysis for model building"

		data = computeResults(beta,numberNode)

		X = numpy.array(data["X"])
		Y = numpy.array(data["Y"])
		Z = numpy.array(data["Z"])
		E = numpy.array(data["Energy"])

		energyParameters = buildModel(E,X,Y,Z)
		[ma,ea,md,ed,mz,ez,c] = energyParameters

		return energyParameters

	def buildModel(output,x,y,z):
		"""function to build a model from a number of parameters"""

		def residuals(parameters,output,x,y,z):

			return output-energyModel(parameters,x,y,z)

		#preliminary model parameters
		[ma,ea,md,ed,mz,ez,c] = [0.05,0.8,1,1,0.8,1.1,100]
		parameters = numpy.array([ma,ea,md,ed,mz,ez,c])
		#model arguments
		arguments = (output,x,y,z)
		#compute least squares regression
		result,sucess = scipy.optimize.leastsq(residuals,parameters,arguments)

		return result

	return collectResults()

def getEquation(beta=None,numberNode=None):
	"function to return the equation of either height or distance for the given number of nodes"

	if (numberNode and beta):

		filename = "results/model_variables.csv"
		variables = loadData(filename)

		numberNodes = variables["N"]
		betas = variables["A"]

		nodeIndexs = [i for i in range(len(numberNodes)) if numberNode == numberNodes[i]]
		betaDiffs = [abs(beta-betas[index]) for index in nodeIndexs]
		index = nodeIndexs[betaDiffs.index(min(betaDiffs))]

		#set the energy model parameters
		[ma,ea,md,ed,mz,ez,c] = [
			variables["ma"][index],
			variables["ea"][index],
			variables["md"][index],
			variables["ed"][index],
			variables["mz"][index],
			variables["ez"][index],
			variables["c"][index]
			]
		equation = "E={:0.2f}(xy)^{{{:0.3f}}}+{:0.2f}abs(x-y)+{:0.2f}z^{{{:0.3f}}}+{:0.0f}".format(ma,ea,md,mz,ez,c)
	else:
		#if there are no beta or numberNode set then return the stock equation
		[ma,ea,md,ed,mz,ez,c] = ["ma","ea","md","ed","mz","ez","c"]
		equation = r"E={}\cdot (xy)^{{{}}}+{}\cdot abs(x-y)+{}\cdot z^{{{}}}+{}".format(ma,ea,md,mz,ez,c)

	return equation

def collectAllResults():
	"collects all results for the length width height model"

	#define nodes and betas from shared variables
	numberNodes = ALL_NODES
	betas = ALL_BETAS

	variables = {
		"A"		:[],
		"N"		:[],
		"ma"	:[],
		"ea"	:[],
		"md"	:[],
		"ed"	:[],
		"mz"	:[],
		"ez"	:[],
		"c"		:[]
	}

	for numberNode in numberNodes:
		for beta in betas:
			variables["A"].append(round(beta,1))
			variables["N"].append(int(numberNode))
			energyParameters = returnModel(beta,numberNode)
					
			[ma,ea,md,ed,mz,ez,c] = energyParameters
			variables["ma"].append(ma)
			variables["ea"].append(ea)
			variables["md"].append(md)
			variables["ed"].append(ed)
			variables["mz"].append(mz)
			variables["ez"].append(ez)
			variables["c"].append(c)

	filename = "results/model_variables.csv"
	saveData(filename,variables)

def computeAllResults(newSample):
	"""function to compute all length width height results possible

	this function uses a csv sample planner so can be run on multiple interpriters
	thus allowing full processor utilisation
	"""

	filename = "sample_plan.csv"
	if newSample:
		data = {
                        "numberNode":ALL_NODES*len(ALL_BETAS)+["END"],
                        "beta":[ALL_BETAS[i//len(ALL_NODES)] for i in range(len(ALL_NODES)*len(ALL_BETAS))]+["END"]
			#"numberNode":[ALL_NODES[i//len(ALL_BETAS)] for i in range(len(ALL_NODES)*len(ALL_BETAS))],
			#"beta":ALL_BETAS*len(ALL_NODES)*len(ALL_BETAS)
			}
		saveData(filename,data)

	while not newSample:
		#load the test case data
		data = loadData(filename)

		#break the while loop if there are no tests left to compute
		if ((len(data["beta"]) == 0) or (len(data["numberNode"]) == 0)):
			break

		#remove test values from file data
		beta = round(float(data["beta"].pop(0)),1)
		numberNode = int(data["numberNode"].pop(0))

		#print the current test case
		print(beta,numberNode)

		try:
			#attempt to save the sample file with the current test cases removed
			saveData(filename,data)
			try:
				#attempt to compute the model with given parameters
				returnModel(beta,numberNode)
			except Exception as exception:
				#if there is a problem print the error
				print("Problem with node: {} a: {} \n {}".format(numberNode,beta,exception))
				#return the current test case to the sample plan
				data["beta"].insert(0,beta)
				data["numberNode"].insert(0,numberNode)
				saveData(filename,data)
		except PermissionError:
			print("Sleep")
			time.sleep(20)


if (__name__ == "__main__"):
	collectAllResults()
        #computeAllResults(False)

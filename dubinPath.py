from shared import *
import numpy,plot

def linePath(startPoint,endPoint,distanceOnly=True):
	"draws a line with the given start and end points"

	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)
	distance = numpy.linalg.norm(endPoint - startPoint)

	if distanceOnly:
		return distance

	x = [startPoint[0],endPoint[0]]
	y = [startPoint[1],endPoint[1]]
	z = [startPoint[2],endPoint[2]]

	mode = "straight"
	height = endPoint[2]-startPoint[2]
	path = [x,y,z]

	return (mode,distance,height,path)

def arcPath(centre,startPoint,endPoint,direction,distanceOnly=True):
	"draws an arc with the given centre and radius given the start and end points"

	centre = numpy.array(centre)
	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)

	#2D problem 
	radiusA = numpy.linalg.norm(startPoint[:2]-centre)
	radiusB = numpy.linalg.norm(endPoint[:2]-centre)
	radius = max(radiusA,radiusB)
	
	[X1,Y1] = startPoint[:2] - centre
	[X2,Y2] = endPoint[:2] - centre
	startAngle = numpy.arctan2(Y1,X1)
	endAngle = numpy.arctan2(Y2,X2)

	if ((startAngle<endAngle) and direction == "R"):
		startAngle += 2*numpy.pi
	elif ((startAngle>endAngle) and direction == "L"):
		endAngle += 2*numpy.pi

	theta = abs(startAngle - endAngle)
	distance = radius*theta

	if distanceOnly:
		return distance

	#compute path
	N = 50
	thetas = numpy.linspace(startAngle,endAngle,N)
	x = centre[0] + radius*numpy.cos(thetas)
	y = centre[1] + radius*numpy.sin(thetas)

	#3D results
	z = numpy.linspace(startPoint[2],endPoint[2],N)
	mode = "turn"
	height = endPoint[2]-startPoint[2]
	distance = numpy.sqrt(distance**2+height**2)
	path = [x,y,z]

	return (mode,distance,height,path)

def tangentLines(centre1,centre2,radius,pathType):
	"""returns the tangent points between two circles with given orientation
	logic from document: http://gieseanw.files.wordpress.com/2012/10/dubins.pdf By Andy Giese
	"""

	#assign both radius to the same
	radius1 = radius2 = radius

	#convert to numpy array for calculation
	centre1 = numpy.array(centre1)
	centre2 = numpy.array(centre2)

	#compute connecting vector
	vector = centre1 - centre2
	distance = numpy.linalg.norm(vector)
	
	#define tangent points based on configuration
	if (pathType == "LSL"):
		ratio = (radius2-radius1)/distance
		if ((ratio < -1) or (ratio > 1)):
			if DEBUG: print("Path Type {} is not possible for inputs".format(pathType))
			return None,None
		angle = numpy.arccos(ratio)
		normal = computeVector(vector,angle)
		point1 = centre1 + normal*radius1
		point2 = centre2 + normal*radius2
	elif (pathType == "RSR"):
		ratio = -(radius2-radius1)/distance
		if ((ratio < -1) or (ratio > 1)):
			if DEBUG: print("Path Type {} is not possible for inputs".format(pathType))
			return None,None
		angle = numpy.arccos(ratio)
		normal = computeVector(-vector,angle)
		point1 = centre1 + normal*radius1
		point2 = centre2 + normal*radius2
	elif (pathType == "LSR"):
		ratio = -(radius2+radius1)/distance
		if ((ratio < -1) or (ratio > 1)):
			if DEBUG: print("Path Type {} is not possible for inputs".format(pathType))
			return None,None
		angle = numpy.arccos(ratio)
		normal = computeVector(vector,angle)
		point1 = centre1 + normal*radius1
		point2 = centre2 - normal*radius2
	elif (pathType == "RSL"):
		ratio = (radius2+radius1)/distance
		if ((ratio < -1) or (ratio > 1)):
			if DEBUG: print("Path Type {} is not possible for inputs".format(pathType))
			return None,None
		angle = numpy.arccos(ratio)
		normal = computeVector(-vector,angle)
		point1 = centre1 + normal*radius1
		point2 = centre2 - normal*radius2

	if (all(numpy.isnan(point1)) or all(numpy.isnan(point2))):
		if DEBUG: print("Path Type {} is not possible for inputs".format(pathType))
		return None,None

	return point1,point2

def tangentCircles(centre1,centre2,radius,pathType):
	"""returns the tangent points between three circles 
	logic from document: http://gieseanw.files.wordpress.com/2012/10/dubins.pdf By Andy Giese
	"""

	#convert to numpy array for calculation
	centre1 = numpy.array(centre1)
	centre2 = numpy.array(centre2)
	
	#compute vector between circle centres and calculate length
	vector1 = centre2-centre1
	length = numpy.linalg.norm(vector1)

	#if length greater than 4 radius return None
	if (length >= 4*radius):
		if DEBUG:
			print("Circle centres are too far apart")
		return None,None,None

	#calculate angle to third circle depending on orientation
	if pathType == "LRL":
		theta = numpy.arccos(length/(4*radius))
	elif pathType == "RLR":
		theta = -numpy.arccos(length/(4*radius))

	#compute vector from first circle to third circle
	vector2 = computeVector(vector1,theta)
	centre3 = centre1 + vector2*2*radius

	#compute vector from second circle to third circle
	vector3 = centre3 - centre2
	vector3 = computeUnitVector(vector3)
	
	#calculate locations of tangents
	startTangent = centre1 + vector2*radius
	endTangent = centre2 + vector3*radius

	return startTangent,endTangent,centre3

def computeVector(vector,angle):
	"computes and returns the normal vector given a vector and angle"

	cosAngle = numpy.cos(angle)
	[v_x,v_y] = vector
	n_x = (v_x * cosAngle) - (v_y * numpy.sqrt(1-cosAngle**2))
	n_y = (v_x * numpy.sqrt(1-cosAngle**2)) + (v_y * cosAngle)
	normal = numpy.array([n_x,n_y])
	normal = computeUnitVector(normal)
	return normal

def computeUnitVector(vector):
	"computes and returns the unit vector of the given vector: vector"

	normal = numpy.linalg.norm(vector)
	if (normal == 0):
		return numpy.array([0]*len(vector))
	else:
		return vector/normal

def computeCentre(point,direction,radius,orientation):
	"""computes the centre point of a circle given:
	point - the coordinates of a point that lies on the circumfrence of a circle
	direction - the direction of heading that is tangential to the circle at the point
	radius - the radius of the circle
	orientation - weather the circle is left or right turn
	"""

	[x,y] = point
	[d_x,d_y] = direction

	point = numpy.array(point)
	direction = numpy.array(direction)

	if (orientation == "L"):
		normal = computeVector(direction,numpy.pi/2)
		centre = point + radius*normal
	elif (orientation == "R"):
		normal = computeVector(-direction,numpy.pi/2)
		centre = point + radius*normal

	return centre
	
def dubinDistance(startPoint,startDirection,endPoint,endDirection,radius,pathType):
	""" computes the lengths of any of the 6 options of dubin paths:
	['RSR','LSL','RSL','LSR','RLR','LRL'] and returns details of each stage of travel and path
	"""

	distances = []
	if (pathType in ['RSR','LSL','RSL','LSR']):

		startCentre = computeCentre(startPoint[:2],startDirection[:2],radius,pathType[0])
		endCentre = computeCentre(endPoint[:2],endDirection[:2],radius,pathType[2])
		startTangent,endTangent = tangentLines(startCentre[:2],endCentre[:2],radius,pathType)

		if (None in [startTangent,endTangent]):
			distances = None
		else:
			distances.append(arcPath(startCentre,startPoint,startTangent,pathType[0]))
			distances.append(linePath(startTangent,endTangent))
			distances.append(arcPath(endCentre,endTangent,endPoint,pathType[2]))

	elif (pathType in ['RLR','LRL']):

		startCentre = computeCentre(startPoint[:2],startDirection[:2],radius,pathType[0])
		endCentre = computeCentre(endPoint[:2],endDirection[:2],radius,pathType[2])
		startTangent,endTangent,middleCentre = tangentCircles(startCentre[:2],endCentre[:2],radius,pathType)

		if None in [startTangent,endTangent,middleCentre]:
			distances = None
		elif all([round(startCentre[i],2) == round(endCentre[i],2) for i in [0,1]]):
			distances.append(arcPath(startCentre,startPoint,endPoint,pathType[0]))
		else:
			distances.append(arcPath(startCentre,startPoint,startTangent,pathType[0]))
			distances.append(arcPath(middleCentre,startTangent,endTangent,pathType[1]))
			distances.append(arcPath(endCentre,endTangent,endPoint,pathType[2]))
	else:
		raise ValueError("Path type {} is not in list ['RSR','LSL','RSL','LSR','RLR','LRL']".format(pathType))

	return distances

def dubinPath(startPoint,startDirection,endPoint,endDirection,radius,pathType,distances=None):
	"""computes the results of any of the 6 options of dubin paths:
	['RSR','LSL','RSL','LSR','RLR','LRL']
	"""

	if not distances:
		distances = dubinDistance(startPoint,startDirection,endPoint,endDirection,radius,pathType)

	startPoint = list(startPoint) + [0]*(3-len(startPoint))
	startDirection = list(startDirection) + [0]*(3-len(startDirection))
	endPoint = list(endPoint) + [0]*(3-len(endPoint))
	endDirection = list(endDirection) + [0]*(3-len(endDirection))

	height = endPoint[2]-startPoint[2]

	results = []
	if (pathType in ['RSR','LSL','RSL','LSR']):

		startCentre = computeCentre(startPoint[:2],startDirection[:2],radius,pathType[0])
		endCentre = computeCentre(endPoint[:2],endDirection[:2],radius,pathType[2])
		startTangent,endTangent = tangentLines(startCentre[:2],endCentre[:2],radius,pathType)

		if (None in [startTangent,endTangent]):
			results = None
		else:
			startTangent = [i for i in startTangent]+[startPoint[2]+height*distances[0]/sum(distances)]
			endTangent = [i for i in endTangent]+[endPoint[2]-height*distances[-1]/sum(distances)]
			results.append(arcPath(startCentre,startPoint,startTangent,pathType[0],False))
			results.append(linePath(startTangent,endTangent,False))
			results.append(arcPath(endCentre,endTangent,endPoint,pathType[2],False))

	elif (pathType in ['RLR','LRL']):

		startCentre = computeCentre(startPoint[:2],startDirection[:2],radius,pathType[0])
		endCentre = computeCentre(endPoint[:2],endDirection[:2],radius,pathType[2])
		startTangent,endTangent,middleCentre = tangentCircles(startCentre[:2],endCentre[:2],radius,pathType)

		if None in [startTangent,endTangent,middleCentre]:
			results = None
		elif all([round(startCentre[i],2) == round(endCentre[i],2) for i in [0,1]]):
			results.append(arcPath(startCentre,startPoint,endPoint,pathType[0],False))
		else:
			startTangent = [i for i in startTangent]+[startPoint[2]+height*distances[0]/sum(distances)]
			endTangent = [i for i in endTangent]+[endPoint[2]-height*distances[-1]/sum(distances)]
			results.append(arcPath(startCentre,startPoint,startTangent,pathType[0],False))
			results.append(arcPath(middleCentre,startTangent,endTangent,pathType[1],False))
			results.append(arcPath(endCentre,endTangent,endPoint,pathType[2],False))
	else:
		raise ValueError("Path type {} is not in list ['RSR','LSL','RSL','LSR','RLR','LRL']".format(pathType))

	return results

def bestPath(startPoint,startDirection,endPoint,endDirection,radius):
	"computes the length of the best dubin path and returns route of the shortest"

	bestResults = None
	bestDistances = [numpy.infty]

	#cycle through options calculating distance
	for pathType in ['RSR','LSL','RSL','LSR','RLR','LRL']:

		distances = dubinDistance(startPoint,startDirection,endPoint,endDirection,radius,pathType)

		if (distances and (sum(distances) < sum(bestDistances))):
			bestPath = pathType
			bestDistances = distances

	return dubinPath(startPoint,startDirection,endPoint,endDirection,radius,bestPath,bestDistances)

class DubinPath():
	"""DubinPath is a class to enable calculation and plotting of the minimum length route through
	a number of nodes
	For each additional node DubinPath adds the energy distance and path to the class variables
	"""

	def __init__(self, radius, planeModel=None):

		self.planeModel = planeModel
		self.radius = radius
		self.distance = 0
		self.energy = 0
		self.nodes = []
		self.lastNodes = [None,None]

		self.x,self.y,self.z = [],[],[]
		
	def addNode(self,node):
		"method to add a node to the route"

		self.nodes.append(numpy.array(node))
		nodeCount = len(self.nodes)
		radius = self.radius

		if (nodeCount>2):
			previousNode = self.nodes[-3]
			startNode = self.nodes[-2]
			endNode = self.nodes[-1]
			startDirection = startNode - previousNode
			endDirection = endNode - startNode

			results = bestPath(startNode,startDirection,endNode,endDirection,self.radius)

			for result in results:
				mode,distance,height,path = result

				self.distance += distance
				self.x += [i for i in path[0]]
				self.y += [i for i in path[1]]
				self.z += [i for i in path[2]]

				if self.planeModel:
					if (mode == "straight"):
						self.energy += self.planeModel.climbingFlight(distance,height)
					elif (mode == "turn"):
						self.energy += self.planeModel.climbingTurningFlight(distance,height,radius)
					else:
						raise ValueError("The mode of flight needs to be straight or turning")

		elif (nodeCount>1):
			self.lastNodes[1] = node
		elif (nodeCount>0):
			self.lastNodes[0] = node

	def makeLoop(self):
		"method to complete the paths loop"

		for i in range(len(self.lastNodes)):
			if self.lastNodes[i] != None:
				self.addNode(self.lastNodes[i])
				self.lastNodes[i] = None

	def getDistance(self):
		"method to return the distance of the path"

		self.makeLoop()
		return self.distance

	def getPath(self):
		"method to return the points of the path "

		self.makeLoop()
		return [self.x,self.y,self.z]

	def getEnergy(self):
		"returns the energy required to navigate the given path"

		self.makeLoop()
		return self.energy
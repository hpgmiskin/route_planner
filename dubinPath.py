#code to calculate and plot dubin paths

from shared import *
import numpy
import matplotlib.pyplot as pyplot

DEBUG = False

def drawLine(startPoint,endPoint):
	"draws a line with the given start and end points"

	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)
	distance = numpy.linalg.norm(endPoint - startPoint)

	x = [startPoint[0],endPoint[0]]
	y = [startPoint[1],endPoint[1]]

	pyplot.hold(True)
	pyplot.plot(x,y)

	return distance

def drawArc(centre,startPoint,endPoint,direction):
	"draws an arc with the given centre and radius given the start and end points"

	centre = numpy.array(centre)
	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)

	radiusA = numpy.linalg.norm(startPoint-centre)
	radiusB = numpy.linalg.norm(endPoint-centre)

	if (round(radiusA,2) != round(radiusB,2)):
		raise RuntimeWarning("The given start point {} and end point {} do not lie on the circle with centre {}".format(startPoint,endPoint,centre))
	
	radius = max(radiusA,radiusB)
	
	[X1,Y1] = startPoint - centre
	[X2,Y2] = endPoint - centre
	startAngle = numpy.arctan2(Y1,X1)
	endAngle = numpy.arctan2(Y2,X2)

	if ((startAngle<endAngle) and direction == "R"):
		startAngle += 2*numpy.pi
	elif ((startAngle>endAngle) and direction == "L"):
		endAngle += 2*numpy.pi

	thetas = numpy.linspace(startAngle,endAngle,100)
	xLine = centre[0] + radius*numpy.cos(thetas)
	yLine = centre[1] + radius*numpy.sin(thetas)

	xScatter = [centre[0],startPoint[0],endPoint[0]]
	yScatter = [centre[1],startPoint[1],endPoint[1]]

	pyplot.hold(True)
	pyplot.scatter(xScatter,yScatter)
	pyplot.plot(xLine,yLine)

	theta = abs(startAngle - endAngle)
	distance = radius*theta

	return distance

def drawCircle(centre,radius):
	"function to draw a circle"

	theta = numpy.linspace(0,2*numpy.pi,100)

	x = centre[0] + radius*numpy.cos(theta)
	y = centre[1] + radius*numpy.sin(theta)

	pyplot.plot(x,y)
	pyplot.axis('equal')

def tangentLines(centre1,centre2,radius,pathType):
	"""returns the tangent points between two circles with given orientation

	From document: http://gieseanw.files.wordpress.com/2012/10/dubins.pdf
	By Andy Giese
	"""

	#assign both radius to the same
	radius1 = radius2 = radius

	#convert to numpy array for calculation
	centre1 = numpy.array(centre1)
	centre2 = numpy.array(centre2)

	#compute connecting vector
	vector = centre1 - centre2
	distance = numpy.linalg.norm(vector)

	#return None if distance is too small
	if False:#(distance < 4*radius):
		return None,None
	
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

	if DEBUG:
		drawCircle(centre1,radius1)
		drawCircle(centre2,radius2)
		drawLine(point1,point2)

	if (all(numpy.isnan(point1)) and all(numpy.isnan(point2))):
		if DEBUG:
			print("Path Type {} is not possible for inputs".format(pathType))
		return None,None

	return point1,point2

def tangentCircles(centre1,centre2,radius,pathType):
	"""returns the tangent points between three circles 

	From document: http://gieseanw.files.wordpress.com/2012/10/dubins.pdf
	By Andy Giese
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

	if DEBUG:
		drawCircle(centre1,radius)
		drawCircle(centre2,radius)
		drawCircle(centre3,radius)
		pyplot.scatter(startTangent[0],startTangent[1])
		pyplot.scatter(endTangent[0],endTangent[1])

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
		return numpy.array([0,0])
	else:
		return vector/normal

def computeCentre(point,direction,radius,orientation):
	"""computes the centre point of a circle given:

	point - the coordinates of a point that lies on the circumfrence of a circle
	direction - the direction of heading that is tangential to the circle at the point
	radius - the radius of the circle
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

	if DEBUG:
		pyplot.hold(True)
		pyplot.scatter(x,y)
		drawLine(point,point+direction)
		#drawCircle(centre,radius)

	return centre

def dubinPath(startPoint,startDirection,endPoint,endDirection,radius,pathType):
	"""
	computes the lengths of the 6 options of dubin paths:

	['RSR','LSL','RSL','LSR','RLR','LRL']

	and plots each path before selecting the shortest path
	"""

	#print(pathType)

	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)
	startDirection = numpy.array(startDirection)
	endDirection = numpy.array(endDirection)

	if DEBUG:
		print(startPoint,startPoint+startDirection)
		drawLine(startPoint,startPoint+startDirection)
		print(endPoint,endPoint+endDirection)
		drawLine(endPoint,endPoint+endDirection)

	if (all([item==0 for item in startDirection]) or all([item==0 for item in endDirection])):
		print(startDirection,endDirection)
		raise ValueError("Start Directions must not all be negative")

	minDistance = numpy.linalg.norm(endPoint-startPoint)
	distance = 0

	if (pathType in ['RSR','LSL','RSL','LSR']):

		startCentre = computeCentre(startPoint,startDirection,radius,pathType[0])
		endCentre = computeCentre(endPoint,endDirection,radius,pathType[2])
		startTangent,endTangent = tangentLines(startCentre,endCentre,radius,pathType)

		if (None in [startTangent,endTangent]):
			distance = numpy.infty
		else:
			distance += drawArc(startCentre,startPoint,startTangent,pathType[0])
			distance += drawLine(startTangent,endTangent)
			distance += drawArc(endCentre,endTangent,endPoint,pathType[2])

	elif (pathType in ['RLR','LRL']):
		startCentre = computeCentre(startPoint,startDirection,radius,pathType[0])
		endCentre = computeCentre(endPoint,endDirection,radius,pathType[2])

		startTangent,endTangent,middleCentre = tangentCircles(startCentre,endCentre,radius,pathType)

		if None in [startTangent,endTangent,middleCentre]:
			distance = numpy.infty
		elif all([round(startCentre[i],2) == round(endCentre[i],2) for i in [0,1]]):
			distance = drawArc(startCentre,startPoint,endPoint,pathType[0])
		else:
			distance += drawArc(startCentre,startPoint,startTangent,pathType[0])
			distance += drawArc(middleCentre,startTangent,endTangent,pathType[1])
			distance += drawArc(endCentre,endTangent,endPoint,pathType[2])

	else:
		raise ValueError("Path type {} is not in list ['RSR','LSL','RSL','LSR','RLR','LRL']".format(pathType))

	if (distance < numpy.infty) and DEBUG:
		print(distance)
		pyplot.axis('equal')
		pyplot.show()

	return distance

def bestPath(startPoint,startDirection,endPoint,endDirection,radius):
	"computes the length of the best dubin path and returns route of the shortest"

	height = 0
	bestDistance = numpy.infty

	#is given matrixs are in 3 dimensions correct for height
	if (max(len(startPoint),len(endPoint)) > 2):

		#calculate height gain
		height = endPoint[2]-startPoint[2]

		#print(startPoint,startDirection,endPoint,endDirection)

		#reduce to 2D planning problem
		startPoint = startPoint[:2]
		startDirection = startDirection[:2]
		endPoint = endPoint[:2]
		endDirection = endDirection[:2]

		#check height change not too great
		maxDistance = numpy.linalg.norm(endPoint-startPoint) + 2*radius*numpy.pi
		if (calculateEnergy(maxDistance,height) == numpy.infty):
			return None,numpy.infty


	#cycle through options calculating distance
	for pathType in ['RSR','LSL','RSL','LSR','RLR','LRL']:

		if DEBUG: print(pathType)

		#print(startPoint,startDirection,endPoint,endDirection)
		distance = dubinPath(startPoint,startDirection,endPoint,endDirection,radius,pathType)
		
		if (distance < bestDistance):
			bestPath = pathType
			bestDistance = distance

	distance = numpy.linalg.norm([distance,height])

	return pathType,calculateEnergy(distance,height)

if __name__ == "__main__":

	# bestPath([0,0],[0,1],[0,2],[0,1],1)
	# bestPath([0,0],[0,1],[2,2],[1,0],1)
	bestPath([0,0],[0,1],[1,2],[1,0],2)
	# bestPath([0,0],[0,-1],[2,2],[1,0],1)
	# bestPath([6,0],[0,-1],[6,2],[1,1],1)

	# dubinPath([0,0],[0,1],[2,2],[1,0],1,'RLR')
	# dubinPath([0,0],[0,1],[1,1],[1,0],1,'RLR')
	# dubinPath([0,0],[0,1],[1,1],[1,0],1,'LRL')
	# dubinPath([0,0],[1,0],[2,2],[1,0],1,'RLR')
	# dubinPath([0,0],[0,1],[2,2],[1,0],1,'LRL')
	# dubinPath([0,0],[0,1],[4,4],[1,0],1,'RSR')
	# dubinPath([0,0],[0,1],[4,4],[1,0],1,'LSL')
	# dubinPath([0,0],[0,1],[4,4],[1,0],1,'LSR')
	# dubinPath([0,0],[0,1],[4,4],[1,0],1,'RSL')
	# dubinPath([0,0],[0,-1],[4,4],[1,0],1,'RSR')
	# dubinPath([0,0],[0,-1],[4,4],[1,0],1,'LSL')
	# dubinPath([0,0],[0,-1],[4,4],[1,0],1,'LSR')
	# dubinPath([0,0],[0,-1],[4,4],[1,0],1,'RSL')

	# computeCentre([0,0],[1,0],1)
	# computeCentre([1,1],[1,1],1)
	# computeCentre([0,0],[0,1],1)
	# computeCentre([0,0],[-1,-1],1)

	#tangentNodes = tangentLines([-1,0],1,[2,0],1)
	#tangentLines([-5,5],1,[2,0],3)
	#tangentLines([-5,5],6,[12,0],3)


	# drawArc([0,0],[-1,0],[0,1])
	# drawLine([0,1],[0,0])
	# drawArc([0,1],[0,0],[0,2])
	# drawLine([0,2],[5,4])
	# drawArc([0,0],[5,4],[4,5])
	# pyplot.show()

#code to calculate and plot dubin paths

import numpy
import matplotlib.pyplot as pyplot

def drawLine(startPoint,endPoint):
	"draws a line with the given start and end points"

	x = [startPoint[0],endPoint[0]]
	y = [startPoint[1],endPoint[1]]

	pyplot.hold(True)
	pyplot.plot(x,y)

def drawArc(centre,startPoint,endPoint):
	"draws an arc with the given centre and radius given the start and end points"

	centre = numpy.array(centre)
	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)

	radiusA = numpy.linalg.norm(startPoint-centre)
	radiusB = numpy.linalg.norm(endPoint-centre)

	if (round(radiusA,2) != round(radiusB,2)):
		raise ValueError("The given start and end points do not lie on the circle with centre {}".format(centre))
	else:
		radius = max(radiusA,radiusB)
	
	[X1,Y1] = startPoint - centre
	[X2,Y2] = endPoint - centre
	startAngle = numpy.arctan2(Y1,X1)
	endAngle = numpy.arctan2(Y2,X2)

	if (endAngle < startAngle):
		endAngle += 2*numpy.pi

	theta = numpy.linspace(startAngle,endAngle,100)
	xLine = centre[0] + radius*numpy.cos(theta)
	yLine = centre[1] + radius*numpy.sin(theta)

	xScatter = [centre[0],startPoint[0],endPoint[0]]
	yScatter = [centre[1],startPoint[1],endPoint[1]]

	pyplot.hold(True)
	pyplot.scatter(xScatter,yScatter)
	pyplot.plot(xLine,yLine)

	return xLine,yLine

def drawCircle(centre,radius):
	"function to draw a circle"

	theta = numpy.linspace(0,2*numpy.pi,100)

	x = centre[0] + radius*numpy.cos(theta)
	y = centre[1] + radius*numpy.sin(theta)

	pyplot.plot(x,y)
	pyplot.axis('equal')

def tangentLines(centre1,radius1,centre2,radius2):
	"""returns the tangent lines between two circles

	From document: http://gieseanw.files.wordpress.com/2012/10/dubins.pdf
	By Andy Giese
	"""

	#convert to numpy array for calculation
	centre1 = numpy.array(centre1)
	centre2 = numpy.array(centre2)

	#draw given circles and connecting line
	drawCircle(centre1,radius1)
	drawCircle(centre2,radius2)
	#drawLine(centre1,centre2)

	#compute connecting vector
	vector = centre1 - centre2
	distance = numpy.linalg.norm(vector)
	
	#compute normal vectors
	angle = (radius2-radius1)/distance
	normal1 = computeNormal(vector,angle)
	normal2 = computeNormal(-vector,-angle)
	angle = (radius2+radius1)/distance
	normal3 = computeNormal(vector,-angle)
	normal4 = computeNormal(-vector,angle)
	
	#compute tangent points for non crossover
	t1 = centre1 + normal1*radius1
	t2 = centre2 + normal1*radius2
	t3 = centre1 + normal2*radius1
	t4 = centre2 + normal2*radius2
	drawLine(t1,t2)
	drawLine(t3,t4)

	#compute tangent points for crossover
	t5 = centre1 + normal3*radius1
	t6 = centre2 - normal3*radius2
	t7 = centre1 + normal4*radius1
	t8 = centre2 - normal4*radius2
	drawLine(t5,t6)
	drawLine(t7,t8)

	pyplot.show()

def computeNormal(vector,angle):
	"computes and returns the normal vector given a vector and angle"

	[v_x,v_y] = vector
	n_x = (v_x * angle) - (v_y * numpy.sqrt(1-angle**2))
	n_y = (v_x * numpy.sqrt(1-angle**2)) + (v_y * angle)
	normal = numpy.array([n_x,n_y])
	normal = normal/numpy.linalg.norm(normal)

	return normal

if __name__ == "__main__":

	tangentLines([-1,0],1,[2,0],1.5)
	tangentLines([-5,5],1,[2,0],3)
	tangentLines([-5,5],6,[12,0],3)


	# drawArc([0,0],[-1,0],[0,1])
	# drawLine([0,1],[0,0])
	# drawArc([0,1],[0,0],[0,2])
	# drawLine([0,2],[5,4])
	# drawArc([0,0],[5,4],[4,5])
	# pyplot.show()

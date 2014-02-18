#code to calculate and plot dubin paths

import numpy
import matplotlib.pyplot as pyplot

def drawArc(centre,startPoint,endPoint):
	"draws an arc with the given centre and radius given the start and end points"

	centre = numpy.array(centre)
	startPoint = numpy.array(startPoint)
	endPoint = numpy.array(endPoint)

	radiusA = numpy.linalg.norm(startPoint-centre)
	radiusB = numpy.linalg.norm(endPoint-centre)

	if (round(radiusA,2) != round(radiusB,2)):
		raise ValueError("The given start and end points do not lie on the circle with centre {}".format(centre))
	
	radius = radiusA

	startAngle = polarArgument(startPoint - centre)
	endAngle = polarArgument(endPoint - centre)

	#print(startAngle,endAngle)

	if (endAngle < startAngle):
		endAngle += 2*numpy.pi

	theta = numpy.linspace(startAngle,endAngle,100)

	x = centre[0] + radius*numpy.cos(theta)
	y = centre[1] + radius*numpy.sin(theta)

	pyplot.hold(True)
	pyplot.scatter(centre[0],centre[1])
	pyplot.scatter(startPoint[0],startPoint[1])
	pyplot.scatter(endPoint[0],endPoint[1])
	pyplot.plot(x,y)
	pyplot.show()

	return x,y

def polarArgument(point):
	"returns the argument of the given point"

	[x,y] = point

	#return simple polars
	if ((x == 0) and (y == 0)):
		return None
	elif (x == 0):
		if (y > 0):
			return numpy.pi/2
		else:
			return 3*numpy.pi/2
	elif (y == 0):
		if (x > 0):
			return 0
		else:
			return numpy.pi

	angle = numpy.arctan(y/x)

	if ((x > 0) and (y > 0)):
		#++
		return angle
	elif ((x < 0) and (y > 0)):
		#-+
		return numpy.pi + angle
	elif ((x < 0) and (y < 0)):
		#--
		return numpy.pi + angle
	elif ((x > 0) and (y < 0)):
		#--
		return 2*numpy.pi + angle

def drawCircle(centre,radius):
	"function to draw a circle"

	theta = numpy.linspace(0,2*numpy.pi,100)

	x = centre[0] + radius*numpy.cos(theta)
	y = centre[1] + radius*numpy.sin(theta)

	pyplot.plot(x,y)
	pyplot.show()


if __name__ == "__main__":

	drawArc([0,0],[-1,0],[0,1])
	drawArc([0,1],[0,0],[0,2])
	drawArc([0,0],[5,4],[4,5])

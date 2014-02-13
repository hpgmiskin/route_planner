# code to calculate the cost of flight

import scipy.integrate
import numpy,pylab
from math import cos,sin,pi

from shared import *
from airFoil import AirFoil

mass = 6
density = 1
gravity = 9.8
xArea = 1
yArea = 0.1

airFoilType = "naca23015-il"
reynoldsNumber = 100000
airFoil = AirFoil(airFoilType,reynoldsNumber)

def solveVelocity(xVelocity0,power,alpha):
	"""Solves the first order ODE to determine the horizontal velocity of a plane under constant power

	power = thrust power deliverde to air
	alpha = angle of attack of airfoil"""

	times = numpy.linspace(0,100,1000)

	CD = airFoil.getCD(alpha)
	CL = airFoil.getCL(alpha)

	alpha = alpha*pi/180
	
	def dvxdt(xVelocity,time):
		"calculates the horizontal acceleration"

		return power*cos(alpha)/(mass*xVelocity) - (density/(2*mass))*(CD*yArea*cos(alpha)+CL*xArea*sin(alpha))*xVelocity**2

	xVelocitys = scipy.integrate.odeint(dvxdt,xVelocity0,times)
	xVelocitys = numpy.reshape(xVelocitys,len(xVelocitys))
	xAccelerations = [dvxdt(xVelocity,0) for xVelocity in xVelocitys]
	xDisplacement = [scipy.integrate.simps(xVelocitys[:i],times[:i]) for i in range(1,len(times))]

	def dvydt(xVelocity):
		"calculates the vertical acceleration"

		return power*sin(alpha)/(mass*xVelocity) + (density/(2*mass))*(CL*xArea*cos(alpha)-CD*yArea*sin(alpha))*xVelocity**2 - gravity

	yAccelerations = [dvydt(xVelocity) for xVelocity in xVelocitys]
	yAccelerations = numpy.reshape(yAccelerations,len(yAccelerations))

	yVelocitys = [scipy.integrate.simps(yAccelerations[:i],times[:i]) for i in range(1,len(times))]
	yDisplacement = [scipy.integrate.simps(yVelocitys[:i],times[:i]) for i in range(1,len(times))]

	filename = "Horizontal Plane Velocity"
	xLabel = "Time (s)"
	xAxis = times

	yLabel = "Velocity (m/s)"
	yAxis = {"X Velocity":xVelocitys,"Y Velocity":yVelocitys,"Y Acceleration":yAccelerations,"X Acceleration":xAccelerations}
	plot2dFigure(filename,xAxis,yAxis,xLabel,yLabel)

	yLabel = "Displacement (m)"
	yAxis = {"X Displacement":xDisplacement,"Y Displacement":yDisplacement}
	plot2dFigure(filename,xAxis,yAxis,xLabel,yLabel)

def solveForce(alpha):
	"function to solve the force required"

if (__name__ == "__main__"):
	solveVelocity(15,16,0)
from shared import *
import numpy,plot,airFoil

#set standard environmental variables
gravity = 9.81
density = 1.19
viscosity = 1.82*10**-5

#set default plane variables
foilName = "naca23015-il"
mass = 0.64
wingSpan = 1.5
wingArea = 0.204
oswaldFactor = 0.7
minTurnRadius = 20

class PlaneEnergy():
	"""PlaneEnergy is a class designed to similate flight manouvers"""

	def __init__(self, mass, wingSpan, wingArea, oswaldFactor, minTurnRadius=0):
		"method to construct the class with plane variables"

		self.mass = mass
		self.minTurnRadius = minTurnRadius
		self.wingSpan = wingSpan
		self.wingArea = wingArea
		self.wingChord = wingArea/wingSpan
		self.oswaldFactor = oswaldFactor
		self.aspectRatio = wingSpan**2/wingArea
		self.flightVelocity = None

	def setAirFoil(self,foilName,reynoldsNumber=1000000):
		"method to set the airfoil type for the plane"

		self.foilName = foilName
		self.reynoldsNumber = reynoldsNumber
		self.airFoil = airFoil.AirFoil(foilName,reynoldsNumber)
		return self.setFlightData()

	def setFlightData(self):
		"method to set the attack angle for optimal range"

		#configure attack angles and coeficients from xfoil
		self.attackAngles = self.airFoil.getAoAs()
		self.cLifts = self.airFoil.getCLs()
		self.cZeroDrags = self.airFoil.getCDs()

		#set coeficient of drag including induced drag
		self.cDrags = self.cZeroDrags + (self.cLifts**2)/(numpy.pi*self.aspectRatio*self.oswaldFactor)
		#define the different sides of range equation for minimisation
		rangeEquation = abs(self.cLifts - numpy.sqrt(self.cZeroDrags*numpy.pi*self.aspectRatio*self.oswaldFactor))
		#minimise range equation to select flight data for best range
		index = numpy.where(rangeEquation==min(rangeEquation))

		#set angle of attack, coeficient of lift and coeficient of drag
		self.attackAngle = self.attackAngles[index]
		self.cLift = self.cLifts[index]
		self.cDrag = self.cDrags[index]

		#if no flight velocity set configure flight velocity
		if not self.flightVelocity:
			self.setFlightVelocity()
			return self.flightVelocity

		#return the reynolds number
		return self.reynoldsNumber

	def checkReynoldsNumber(self):
		"method to check the configured reynolds number complies with the flight velocity"

		#if no veloicty use max range velocity
		if not self.flightVelocity:
			self.setFlightVelocity()

		#calculate the reynolds number from flight velocity
		calculatedReynoldsNumber = float((density*self.wingChord*self.flightVelocity)/viscosity)
		newReynoldsNumber = self.airFoil.setReynoldsNumber(calculatedReynoldsNumber)

		#if reynolds number changed return new velocity
		if (newReynoldsNumber != self.reynoldsNumber):
			self.reynoldsNumber = newReynoldsNumber
			return self.setFlightData()
		else:
			return self.reynoldsNumber

	def setFlightVelocity(self,manualVelocity=None):
		"method to set the cruise velocity either manually or from angle of attack"

		#use given velocity else select optimal velocity
		if manualVelocity:
			self.flightVelocity = manualVelocity
		else:
			self.flightVelocity = numpy.sqrt((2*self.mass*gravity)/(density*self.wingArea*self.cLift))
		
		#given the flight velocity is set test that reynolds number is adequate
		return self.checkReynoldsNumber()
		
	def levelFlight(self,distance):
		"method to specifiy level flight and return energy required for manouver"

		
		return 0.5*distance*density*self.cDrag*self.wingArea*self.flightVelocity**2

	def climbingFlight(self,distance,height):
		"method to specifiy climbing flight and return the energy required for manouver"

		levelEnergy = self.levelFlight(distance)
		climbEnergy = self.mass*gravity*height
		return levelEnergy+climbEnergy

	def turningFlight(self,distance,turnRadius):
		"method to specifiy turning flight at given turning radius and return the energy required for manouver"

		if turnRadius < self.minTurnRadius:
			print("Minimum turning radius reached {}m".format(self.minTurnRadius))
			turnRadius = self.minTurnRadius

		loadFactor = numpy.sqrt(1+(self.flightVelocity**4)/(gravity*turnRadius)**2)
		return distance*(gravity*self.cDrag*loadFactor*self.mass)/self.cLift

	def climbingTurningFlight(self,distance,height,turnRadius):
		"method to specifiy turning and climbing flight at maximum rate of turn and return the energy required for manouver"

		levelEnergy = self.turningFlight(distance,turnRadius)
		climbEnergy = self.mass*gravity*height
		return levelEnergy+climbEnergy

	def getEnergyCoefficient(self):
		"method to return the energy coeficient beta"

		return float(self.levelFlight(1)/self.climbingFlight(0,1))

	def getEnergyFactor(self):
		"method to return the energy factor gamma"

		return float(self.climbingFlight(0,1))
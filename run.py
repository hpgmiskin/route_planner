from shared import *

from manageData import ManageData
from travellingPlane import TravellingPlane

manageData = ManageData()

numberPoints = [10]#,20,30,40,50,60,70,80,100]
#numberPoints = [10,20,40,80,160,320,640,1280]
costs = {"progressive":[],"greedy":[]}

for n in numberPoints:

	name = "{}_nodes".format(n)
	print(name)
	#manageData.updateData(n)

	#for sort in ["progressive","greedy"]:
	sort = "progressive"

	manageData.loadData(n)
	cost = manageData.sortData(TravellingPlane(sort,"path"))
	manageData.plotData(name+"_"+sort)

	costs[sort].append(cost)

xLabel = "Number of Points"
xAxis = numberPoints

yLabel = "Energy Cost of Route"
yAxis = {"Progressive TSP":costs["progressive"],"Greedy TSP":costs["greedy"]}

plot2dFigure("progressive_greedy_costs",xAxis,yAxis,xLabel,yLabel)